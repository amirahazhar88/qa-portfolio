import pytest


def add_comment(api, token, slug, body="A comment"):
    return api.post(f"/articles/{slug}/comments", token=token, json={"comment": {"body": body}})


class TestComments:
    @pytest.mark.smoke
    def test_a_user_can_comment_and_it_is_listed(self, api, article, other_user):
        response = add_comment(api, other_user.token, article["slug"], "Nice read")

        assert response.status_code == 200
        comment = response.json()["comment"]
        assert comment["body"] == "Nice read"
        assert comment["author"]["username"] == other_user.username
        listing = api.get(f"/articles/{article['slug']}/comments").json()
        assert listing["count"] == 1
        assert [c["id"] for c in listing["comments"]] == [comment["id"]]

    def test_comments_are_public_to_read(self, api, article, other_user):
        add_comment(api, other_user.token, article["slug"])

        assert api.get(f"/articles/{article['slug']}/comments").status_code == 200

    def test_an_empty_comment_is_rejected(self, api, article, other_user):
        assert add_comment(api, other_user.token, article["slug"], body="").status_code == 422

    def test_commenting_on_an_unknown_article_is_not_found(self, api, user):
        assert add_comment(api, user.token, "does-not-exist-x").status_code == 404

    @pytest.mark.smoke
    def test_the_author_can_delete_their_comment(self, api, article, other_user):
        comment = add_comment(api, other_user.token, article["slug"]).json()["comment"]

        response = api.delete(f"/articles/{article['slug']}/comments/{comment['id']}", token=other_user.token)

        assert response.status_code == 200

    @pytest.mark.xfail(strict=True, reason="BUG-007: DELETE comment returns 200 but the comment is not removed")
    def test_a_deleted_comment_is_gone_from_the_list(self, api, article, other_user):
        comment = add_comment(api, other_user.token, article["slug"]).json()["comment"]
        api.delete(f"/articles/{article['slug']}/comments/{comment['id']}", token=other_user.token)

        listing = api.get(f"/articles/{article['slug']}/comments").json()

        assert listing["count"] == 0
