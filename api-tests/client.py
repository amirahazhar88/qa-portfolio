"""A thin wrapper around `requests` for the newsclip REST API."""
from __future__ import annotations

import requests


class Api:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()

    def request(self, method: str, path: str, token: str | None = None, **kwargs) -> requests.Response:
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return self._session.request(
            method, f"{self.base_url}{path}", headers=headers, timeout=10, **kwargs
        )

    def get(self, path: str, token: str | None = None, **kwargs) -> requests.Response:
        return self.request("GET", path, token, **kwargs)

    def post(self, path: str, token: str | None = None, **kwargs) -> requests.Response:
        return self.request("POST", path, token, **kwargs)

    def put(self, path: str, token: str | None = None, **kwargs) -> requests.Response:
        return self.request("PUT", path, token, **kwargs)

    def delete(self, path: str, token: str | None = None, **kwargs) -> requests.Response:
        return self.request("DELETE", path, token, **kwargs)
