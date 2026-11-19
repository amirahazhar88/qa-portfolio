import uuid

import pytest

from conftest import article_payload


class TestCreateArticle:
    @pytest.mark.smoke
    def test_create_returns_the_article_with_defaults(self, api, user, make_article):
        article = make_article(user, tagList=["qa", "api"])

        assert article["slug"]
        assert article["author"]["username"] == user.username
        assert article["favorited"] is False
        assert article["favoritesCount"] == 0
        assert sorted(article["tagList"]) == ["api", "qa"]

    def test_the_slug_is_built_from_the_title(self, api, user, make_article):
        title = f"Hello World {uuid.uuid4().hex[:8]}"

        article = make_article(user, title=title)

        assert article["slug"].lower().startswith("hello-world-")

    @pytest.mark.parametrize("missing", ["title", "description", "body"])
    def test_a_missing_field_is_rejected(self, api, user, missing):
        payload = article_payload()
        del payload["article"][missing]

        assert api.post("/articles", token=user.token, json=payload).status_code == 422

    def test_a_duplicate_title_is_a_conflict(self, api, user, article):
        payload = article_payload(title=article["title"])

        assert api.post("/articles", token=user.token, json=payload).status_code == 409

    def test_creating_requires_a_token(self, api):
        assert api.post("/articles", json=article_payload()).status_code == 401


class TestReadArticle:
    def test_anyone_can_read_an_article(self, api, article):
        response = api.get(f"/articles/{article['slug']}")

        assert response.status_code == 200
        assert response.json()["article"]["title"] == article["title"]

    def test_an_unknown_slug_is_not_found(self, api):
        assert api.get(f"/articles/does-not-exist-{uuid.uuid4().hex[:8]}").status_code == 404


class TestUpdateAndDelete:
    @pytest.mark.smoke
    def test_the_author_can_update_an_article(self, api, user, article):
        response = api.put(f"/articles/{article['slug']}", token=user.token, json={"article": {"body": "Edited"}})

        assert response.status_code == 200
        assert api.get(f"/articles/{article['slug']}").json()["article"]["body"] == "Edited"

    @pytest.mark.smoke
    def test_the_author_can_delete_an_article(self, api, user, article):
        assert api.delete(f"/articles/{article['slug']}", token=user.token).status_code == 200

        assert api.get(f"/articles/{article['slug']}").status_code == 404


class TestListArticles:
    def test_the_list_has_articles_and_a_count(self, api, article):
        body = api.get("/articles").json()

        assert isinstance(body["articles"], list)
        assert body["articlesCount"] >= 1

    def test_limit_caps_the_page_size(self, api, user, make_article):
        for _ in range(3):
            make_article(user)

        body = api.get("/articles", params={"limit": 2}).json()

        assert len(body["articles"]) == 2
        assert body["articlesCount"] >= 3

    def test_filter_by_author(self, api, user, other_user, make_article):
        mine = make_article(user)
        make_article(other_user)

        body = api.get("/articles", params={"author": user.username}).json()

        assert [a["slug"] for a in body["articles"]] == [mine["slug"]]
        assert body["articlesCount"] == 1

    def test_filter_by_tag(self, api, user, make_article):
        tag = f"t{uuid.uuid4().hex[:8]}"
        tagged = make_article(user, tagList=[tag])
        make_article(user)

        body = api.get("/articles", params={"tag": tag}).json()

        assert [a["slug"] for a in body["articles"]] == [tagged["slug"]]

    def test_filter_by_favorited(self, api, user, other_user, make_article):
        liked = make_article(other_user)
        make_article(other_user)
        api.post(f"/articles/{liked['slug']}/favorite", token=user.token)

        body = api.get("/articles", params={"favorited": user.username}).json()

        assert [a["slug"] for a in body["articles"]] == [liked["slug"]]

    def test_a_non_numeric_limit_is_rejected(self, api):
        assert api.get("/articles", params={"limit": "abc"}).status_code == 422

    @pytest.mark.xfail(strict=True, reason="BUG-006: a negative limit returns 500, not 422")
    def test_a_negative_limit_is_rejected(self, api):
        assert api.get("/articles", params={"limit": -1}).status_code == 422

    @pytest.mark.xfail(strict=True, reason="BUG-001: offset is multiplied by limit, so later pages are empty")
    def test_the_second_page_has_the_remaining_articles(self, api, user, make_article):
        tag = f"t{uuid.uuid4().hex[:8]}"
        for _ in range(3):
            make_article(user, tagList=[tag])

        body = api.get("/articles", params={"tag": tag, "limit": 2, "offset": 2}).json()

        assert body["articlesCount"] == 3
        assert len(body["articles"]) == 1


class TestFeed:
    def test_the_feed_requires_a_token(self, api):
        assert api.get("/articles/feed").status_code == 401

    def test_a_new_user_has_an_empty_feed(self, api, user):
        body = api.get("/articles/feed", token=user.token).json()

        assert body["articles"] == []
        assert body["articlesCount"] == 0

    @pytest.mark.smoke
    def test_the_feed_shows_articles_from_followed_authors_only(self, api, user, other_user, new_user, make_article):
        stranger = new_user()
        followed = make_article(other_user)
        make_article(stranger)
        api.post(f"/profiles/{other_user.username}/follow", token=user.token)

        body = api.get("/articles/feed", token=user.token).json()

        assert [a["slug"] for a in body["articles"]] == [followed["slug"]]


class TestTags:
    def test_a_created_tag_appears_in_the_tag_list(self, api, user, make_article):
        tag = f"t{uuid.uuid4().hex[:8]}"
        make_article(user, tagList=[tag])

        assert tag in api.get("/tags").json()["tags"]


class TestSoftDeleteIsHiddenByTheApi:
    """The database keeps child rows (tags, comments, favorites) as 'active' after an article is
    soft-deleted; the API must still hide everything that belonged to it. See sql/ for the table view."""

    def test_the_tags_of_a_deleted_article_leave_the_tag_list(self, api, user, make_article):
        tag = f"t{uuid.uuid4().hex[:8]}"
        article = make_article(user, tagList=[tag])
        assert tag in api.get("/tags").json()["tags"]

        api.delete(f"/articles/{article['slug']}", token=user.token)

        assert tag not in api.get("/tags").json()["tags"]
        assert api.get("/articles", params={"tag": tag}).json()["articlesCount"] == 0

    def test_the_comments_of_a_deleted_article_are_not_reachable(self, api, user, other_user, make_article):
        article = make_article(user)
        api.post(f"/articles/{article['slug']}/comments", token=other_user.token, json={"comment": {"body": "hi"}})

        api.delete(f"/articles/{article['slug']}", token=user.token)

        assert api.get(f"/articles/{article['slug']}/comments").status_code == 404
