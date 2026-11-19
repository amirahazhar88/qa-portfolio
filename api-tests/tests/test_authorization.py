"""Who may do what: unauthenticated callers (401) and other users (403)."""
import pytest

from conftest import article_payload


class TestOtherUsersCannotChangYourContent:
    def test_another_user_cannot_update_an_article(self, api, article, other_user):
        response = api.put(f"/articles/{article['slug']}", token=other_user.token, json={"article": {"body": "hacked"}})

        assert response.status_code == 403
        assert api.get(f"/articles/{article['slug']}").json()["article"]["body"] == article["body"]

    def test_another_user_cannot_delete_an_article(self, api, article, other_user):
        response = api.delete(f"/articles/{article['slug']}", token=other_user.token)

        assert response.status_code == 403
        assert api.get(f"/articles/{article['slug']}").status_code == 200

    def test_another_user_cannot_delete_a_comment(self, api, article, user, other_user):
        comment = api.post(
            f"/articles/{article['slug']}/comments", token=user.token, json={"comment": {"body": "mine"}}
        ).json()["comment"]

        response = api.delete(f"/articles/{article['slug']}/comments/{comment['id']}", token=other_user.token)

        assert response.status_code == 403
        assert api.get(f"/articles/{article['slug']}/comments").json()["count"] == 1


# (method, path template, json body): every write endpoint must reject callers without a token.
PROTECTED = [
    ("POST", "/articles", article_payload()),
    ("PUT", "/articles/{slug}", {"article": {"body": "x"}}),
    ("DELETE", "/articles/{slug}", None),
    ("GET", "/articles/feed", None),
    ("POST", "/articles/{slug}/favorite", None),
    ("DELETE", "/articles/{slug}/favorite", None),
    ("POST", "/articles/{slug}/comments", {"comment": {"body": "x"}}),
    ("DELETE", "/articles/{slug}/comments/some-id", None),
    ("POST", "/profiles/{username}/follow", None),
    ("DELETE", "/profiles/{username}/follow", None),
    ("GET", "/user", None),
    ("PUT", "/user", {"user": {"bio": "x"}}),
]


@pytest.mark.parametrize("method,path,body", PROTECTED, ids=[f"{m} {p}" for m, p, _ in PROTECTED])
def test_endpoints_that_change_data_require_a_token(api, article, user, method, path, body):
    path = path.format(slug=article["slug"], username=user.username)

    response = api.request(method, path, json=body)

    assert response.status_code == 401
