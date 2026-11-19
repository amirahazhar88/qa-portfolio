import pytest


class TestFavorites:
    @pytest.mark.smoke
    def test_favoriting_marks_the_article_and_counts_it(self, api, article, other_user):
        response = api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        assert response.status_code == 200
        body = response.json()["article"]
        assert body["favorited"] is True
        assert body["favoritesCount"] == 1

    def test_the_count_adds_up_across_users(self, api, article, user, other_user):
        api.post(f"/articles/{article['slug']}/favorite", token=user.token)
        api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        body = api.get(f"/articles/{article['slug']}", token=user.token).json()["article"]

        assert body["favoritesCount"] == 2
        assert body["favorited"] is True

    def test_an_anonymous_reader_sees_the_count(self, api, article, other_user):
        api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        body = api.get(f"/articles/{article['slug']}").json()["article"]

        assert body["favoritesCount"] == 1

    @pytest.mark.xfail(strict=True, reason="BUG-008: favorited is true for everyone once anyone favorites")
    def test_an_anonymous_reader_does_not_see_favorited(self, api, article, other_user):
        api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        assert api.get(f"/articles/{article['slug']}").json()["article"]["favorited"] is False

    @pytest.mark.xfail(strict=True, reason="BUG-008: favorited is true for everyone once anyone favorites")
    def test_a_user_who_did_not_favorite_does_not_see_favorited(self, api, article, other_user, new_user):
        api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)
        bystander = new_user()

        body = api.get(f"/articles/{article['slug']}", token=bystander.token).json()["article"]

        assert body["favorited"] is False

    def test_unfavoriting_reverses_it(self, api, article, other_user):
        api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        response = api.delete(f"/articles/{article['slug']}/favorite", token=other_user.token)

        assert response.status_code == 200
        body = response.json()["article"]
        assert body["favorited"] is False
        assert body["favoritesCount"] == 0

    def test_favoriting_twice_is_rejected(self, api, article, other_user):
        api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        response = api.post(f"/articles/{article['slug']}/favorite", token=other_user.token)

        assert response.status_code == 400

    def test_unfavoriting_something_not_favorited_is_rejected(self, api, article, other_user):
        response = api.delete(f"/articles/{article['slug']}/favorite", token=other_user.token)

        assert response.status_code == 400

    def test_an_unknown_article_is_not_found(self, api, user):
        assert api.post("/articles/does-not-exist-x/favorite", token=user.token).status_code == 404
