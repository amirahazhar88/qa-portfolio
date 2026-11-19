"""Shared fixtures: an API client, throwaway users, and articles that clean up after the test."""
from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest
from dotenv import load_dotenv

from client import Api

# Same repo-root .env the Playwright tests use (see ../.env.example).
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_URL = os.getenv("API_URL", "http://localhost:3100/api")
PASSWORD = "Passw0rd!123"


def unique(prefix: str = "qa") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


@dataclass
class User:
    username: str
    email: str
    password: str
    token: str


def user_payload(username: str | None = None, **overrides) -> dict:
    username = username or unique()
    user = {"username": username, "email": f"{username}@example.com", "password": PASSWORD}
    user.update(overrides)
    return {"user": user}


def article_payload(**overrides) -> dict:
    article = {
        "title": f"QA article {uuid.uuid4().hex[:10]}",  # the slug is built from the title, so keep it unique
        "description": "Created by an API test",
        "body": "Body text for an API test.",
        "tagList": [],
    }
    article.update(overrides)
    return {"article": article}


@pytest.fixture(scope="session")
def api() -> Api:
    return Api(API_URL)


@pytest.fixture
def new_user(api):
    """Factory: register a fresh user and return it."""

    def _create() -> User:
        payload = user_payload()
        response = api.post("/users", json=payload)
        assert response.status_code == 200, response.text
        u = payload["user"]
        return User(u["username"], u["email"], u["password"], response.json()["user"]["token"])

    return _create


@pytest.fixture
def user(new_user) -> User:
    return new_user()


@pytest.fixture
def other_user(new_user) -> User:
    return new_user()


@pytest.fixture
def make_article(api):
    """Factory: create an article as `owner`; every article is deleted again after the test."""
    created: list[tuple[str, str]] = []

    def _create(owner: User, **overrides) -> dict:
        response = api.post("/articles", token=owner.token, json=article_payload(**overrides))
        assert response.status_code == 200, response.text
        article = response.json()["article"]
        created.append((article["slug"], owner.token))
        return article

    yield _create

    for slug, token in created:
        api.delete(f"/articles/{slug}", token=token)  # 404 is fine if the test already deleted it


@pytest.fixture
def article(make_article, user) -> dict:
    return make_article(user)
