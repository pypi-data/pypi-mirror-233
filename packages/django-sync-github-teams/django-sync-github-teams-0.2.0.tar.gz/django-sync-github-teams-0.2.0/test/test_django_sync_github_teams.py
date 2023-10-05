import json
import pytest
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django_sync_github_teams.sync import get_next_link
from django_sync_github_teams.sync import sync_github_teams_on_login
from django_sync_github_teams.sync import sync_github_teams


class TestGetNextLink:
    def test_no_link(self):
        assert get_next_link(None) is None

    def test_github_api_example(self):
        s = '<https://api.github.com/repositories/1300192/issues?page=2>; rel="prev", <https://api.github.com/repositories/1300192/issues?page=4>; rel="next", <https://api.github.com/repositories/1300192/issues?page=515>; rel="last", <https://api.github.com/repositories/1300192/issues?page=1>; rel="first"'
        assert (
            get_next_link(s)
            == "https://api.github.com/repositories/1300192/issues?page=4"
        )

    def test_invalid_input(self):
        assert get_next_link("invalida date") is None


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create(username="foobar")


@pytest.fixture
def github_provider(db):
    return SocialApp.objects.create(provider="github")


@pytest.fixture
def github_account(github_provider, user):
    return SocialAccount.objects.create(provider="github", user=user, uid="77777")


class TestSyncOnLogin:
    def test_no_sync(self, settings, mocker, db):
        sync = mocker.patch("django_sync_github_teams.sync.sync_github_teams")
        sync_github_teams_on_login(None, user=None)
        sync.assert_not_called()

    def test_sync(self, settings, mocker, user, github_account):
        sync = mocker.patch("django_sync_github_teams.sync.sync_github_teams")
        sync_github_teams_on_login(None, user=user)
        sync.assert_called()


class TestSync:
    def test_exit_early_if_unconfigured(self, settings):
        settings.SYNC_GITHUB_TEAMS = []
        sync_github_teams()

    def test_sync(self, settings, requests_mock, db, user, github_account):
        settings.SYNC_GITHUB_TEAMS = ["myorg/myteam"]
        settings.SYNC_GITHUB_TEAMS_TOKEN = "*********************"
        data = json.dumps(
            [
                {
                    "id": github_account.uid,
                }
            ]
        )
        requests_mock.get(
            "https://api.github.com/orgs/myorg/teams/myteam/members", text=data
        )
        sync_github_teams()
        groups = Group.objects.filter(name="myteam")
        assert groups.exists()
        group = groups.get()
        assert list(group.user_set.all()) == [user]

    @pytest.mark.parametrize(
        "sync_github_teams_setting",
        (
            "myorg/team1, myorg/team2",
            "myorg/team1 , myorg/team2",
            "myorg/team1 ,myorg/team2",
            "myorg/team1,myorg/team2",
            "myorg/team1 myorg/team2",
        ),
    )
    def test_sync_settings_as_string(
        self,
        settings,
        requests_mock,
        db,
        user,
        github_account,
        sync_github_teams_setting,
    ):
        settings.SYNC_GITHUB_TEAMS = sync_github_teams_setting
        settings.SYNC_GITHUB_TEAMS_TOKEN = "*********************"
        data = json.dumps(
            [
                {
                    "id": github_account.uid,
                }
            ]
        )
        requests_mock.get(
            "https://api.github.com/orgs/myorg/teams/team1/members", text=data
        )
        requests_mock.get(
            "https://api.github.com/orgs/myorg/teams/team2/members", text=data
        )
        sync_github_teams()
        group1 = Group.objects.get(name="team1")
        group2 = Group.objects.get(name="team2")
        assert list(group1.user_set.all()) == [user]
        assert list(group2.user_set.all()) == [user]
