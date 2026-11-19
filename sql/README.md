# sql

Data integrity checks for the newsclip MySQL database.

```sh
sql/run_checks.sh        # needs the Docker stack (container newsclip-mysql)
```

Each file in `checks/` is one `SELECT` that returns the **offending rows**. No rows means the check passes.

```
PASS   Every article_tag row points at an existing article
XFAIL  Every user email looks like an email address   [2 offending row(s), known: BUG-005 ...]
```

| Result | Meaning |
|---|---|
| `PASS` | no offending rows |
| `FAIL` | offending rows: investigate (data problem or a new bug) |
| `XFAIL` | a **known defect** (`-- known: BUG-nnn` in the file); the run stays green |
| `XPASS` | a known defect no longer reproduces: remove the `-- known` line (fails the run on purpose) |

## What is checked

Orphans where the schema has no foreign key (`article_tag`, `user_follow`), self-follows, valid emails,
case-insensitive uniqueness (usernames, emails, slugs), duplicate favorites and follows, complete articles,
the `record_status` domain, timestamp order, and banned users.

## Things to know about this schema

- **Soft delete.** Rows are never removed; `record_status` becomes `'deleted'`. Filter on `record_status = 'active'` in any new query.
- **Children stay `active` when an article is soft-deleted** (tags, comments, favorites). That is by design: the API hides them through the parent article. `api-tests/` asserts this (`TestSoftDeleteIsHiddenByTheApi`), so it is not a SQL failure.
- **Comments are never marked deleted.** The API says 200 but the row stays `active` (BUG-007).
- The checks run against the whole database, so they also see leftovers from earlier test runs. Reset with `docker compose down -v` for a clean slate.

Credentials default to the public dev values in `newsclip/api/docker-compose.yml`. Override with `MYSQL_CONTAINER`, `MYSQL_USER`, `MYSQL_DATABASE`, `MYSQL_PASSWORD`.

## Adding a check

Copy a file in `checks/`, change the `-- name:`, and write a query that returns the offending rows. Prove it can fail: insert a bad row, run the script, then delete the row.
