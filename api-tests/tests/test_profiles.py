import pytest


class TestProfiles:
    def test_a_profile_is_public(self, api, user):
        response = api.get(f"/profiles/{user.username}")

        assert response.status_code == 200
        profile = response.json()["profile"]
        assert profile["username"] == user.username
        assert profile["following"] is False

    def test_an_unknown_profile_is_not_found(self, api):
        assert api.get("/profiles/nobody-here-xyz").status_code == 404


class TestFollow:
    @pytest.mark.smoke
    def test_following_is_visible_to_the_follower_only(self, api, user, other_user):
        response = api.post(f"/profiles/{other_user.username}/follow", token=user.token)

        assert response.status_code == 200
        assert response.json()["profile"]["following"] is True
        as_follower = api.get(f"/profiles/{other_user.username}", token=user.token).json()["profile"]
        assert as_follower["following"] is True

    def test_a_user_who_does_not_follow_sees_following_false(self, api, user, other_user, new_user):
        api.post(f"/profiles/{other_user.username}/follow", token=user.token)
        bystander = new_user()

        profile = api.get(f"/profiles/{other_user.username}", token=bystander.token).json()["profile"]

        assert profile["following"] is False

    @pytest.mark.xfail(strict=True, reason="BUG-009: following is true for anonymous callers once anyone follows")
    def test_an_anonymous_visitor_does_not_see_following(self, api, user, other_user):
        api.post(f"/profiles/{other_user.username}/follow", token=user.token)

        assert api.get(f"/profiles/{other_user.username}").json()["profile"]["following"] is False

    def test_unfollowing_reverses_it(self, api, user, other_user):
        api.post(f"/profiles/{other_user.username}/follow", token=user.token)

        response = api.delete(f"/profiles/{other_user.username}/follow", token=user.token)

        assert response.status_code == 200
        assert response.json()["profile"]["following"] is False

    def test_you_cannot_follow_yourself(self, api, user):
        assert api.post(f"/profiles/{user.username}/follow", token=user.token).status_code == 400

    def test_following_twice_is_rejected(self, api, user, other_user):
        api.post(f"/profiles/{other_user.username}/follow", token=user.token)

        assert api.post(f"/profiles/{other_user.username}/follow", token=user.token).status_code == 400

    def test_following_an_unknown_user_is_not_found(self, api, user):
        assert api.post("/profiles/nobody-here-xyz/follow", token=user.token).status_code == 404
