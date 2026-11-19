# api-tests

pytest + requests tests for the newsclip REST API (`newsclip/api`, default `http://localhost:3100/api`).

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest                 # everything
.venv/bin/python -m pytest -m smoke        # quick checks
.venv/bin/python -m pytest tests/test_articles.py -k filter
```

`API_URL` comes from the repo-root `.env` (see `../.env.example`) and defaults to `http://localhost:3100/api`.

## Layout

| File | Purpose |
|---|---|
| `client.py` | Small wrapper around `requests` (base URL, optional Bearer token) |
| `conftest.py` | Fixtures: `api`, `user`, `other_user`, `new_user`, `article`, `make_article` (cleans up) |
| `tests/test_users.py` | Register, login, current user, update user |
| `tests/test_articles.py` | CRUD, list filters and pagination, feed, tags |
| `tests/test_authorization.py` | 401 without a token on every protected endpoint; 403 for other users |
| `tests/test_favorites.py`, `test_profiles.py`, `test_comments.py`, `test_health.py` | One area each |

## Known defects

A test for a known bug is marked `@pytest.mark.xfail(strict=True, reason="BUG-nnn: ...")`.
The run stays green while the bug is open. When the bug is fixed the test **fails on purpose** ("XPASS(strict)"),
which is the signal to remove the `xfail` and close the report in `../docs/bugs/`.

```sh
.venv/bin/python -m pytest -rx     # list the expected failures with their reasons
```

## Conventions

- Every test makes its own users and articles with unique names, so tests are independent.
- Articles created through the `make_article` fixture are deleted after the test. Users are not (reset the DB with `docker compose down -v`).
