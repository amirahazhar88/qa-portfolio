# newsclip test summary

| | |
|---|---|
| **Status** | v0.1 |
| **Author** | Amirah Azhar |
| **Date** | 2026-11-19 |
| **Application** | newsclip (`newsclip/`) |
| **Plan** | [test-plan.md](test-plan.md) |
| **Test cases** | [test-cases.md](test-cases.md) |

## 1. Verdict

**Not ready to release.** The automated suites run and are stable, but the exit criteria in the test plan are **not met**: five High-severity defects are open (for example, deleted comments are never removed, and later pages of a filtered list are empty). The full defect list is in section 4.

## 2. What was tested

| Level | Tool | Location | Size |
|---|---|---|---|
| UI end-to-end | Playwright (TypeScript), Chromium | `ui-tests/` | 46 tests |
| API | pytest + requests | `api-tests/` | 89 tests |
| Database | SQL checks run through Docker | `sql/` | 11 checks |

Reporting: one combined **Allure** report (`scripts/report.sh`, published from CI). CI: GitHub Actions starts the API, MySQL and frontend, then runs the SQL checks, the API tests and the UI tests.

## 3. Results (latest full run)

| Suite | Passed | Expected failures (known defects) | Unexpected failures |
|---|---|---|---|
| UI | 46 (includes 4 expected failures) | 4 | 0 |
| API | 79 | 10 | 0 |
| SQL | 10 | 1 | 0 |

An *expected failure* is a test written to fail until a known bug is fixed (`test.fail()` in Playwright, `xfail(strict=True)` in pytest, `-- known:` in SQL). The run stays green while the bug is open, and it **fails on purpose** when the bug is fixed, which is the signal to close the report. In total **15 checks** are tied to a defect.

Feature coverage (see the matrix in the test plan): all P1 and P2 features have UI and API tests. P3 is partly covered. Soft-delete behaviour and data integrity are covered by SQL checks.

## 4. Defects

Nine defects were found and reported in [`docs/bugs/`](bugs/). All are **open**.

| ID | Summary | Severity |
|---|---|---|
| [BUG-001](bugs/BUG-001.md) | Pagination: the API multiplies `offset` by `limit`, so page 2 of a filtered list is empty | High |
| [BUG-002](bugs/BUG-002.md) | Settings cannot be saved with an empty bio or image; the error says "Unable to connect" | High |
| [BUG-003](bugs/BUG-003.md) | Follow on the article page calls `/profiles/undefined/follow` | High |
| [BUG-007](bugs/BUG-007.md) | Deleting a comment returns 200 but the comment is not removed | High |
| [BUG-008](bugs/BUG-008.md) | `favorited` is true for every reader once anyone has favorited an article | High |
| [BUG-004](bugs/BUG-004.md) | Changing email or username to a taken one returns 500 (register returns 409) | Medium |
| [BUG-005](bugs/BUG-005.md) | Registration accepts an invalid email address | Medium |
| [BUG-009](bugs/BUG-009.md) | `following` is true for anonymous callers once anyone follows the user | Medium |
| [BUG-006](bugs/BUG-006.md) | A negative `limit` on the article list returns 500 | Low |

Totals: 0 Critical, 5 High, 3 Medium, 1 Low.

## 5. Exit criteria

| Criterion (from the test plan) | Result |
|---|---|
| 100% of P1 test cases executed and passing | **Not met.** All are executed, but P1 defects BUG-001, BUG-007 and BUG-008 mean those cases cannot pass yet. |
| At least 95% of planned tests executed; at least 90% pass | Executed: met (100% of the 135 automated tests). Pass rate: 121 of 135 = **89.6%** if expected failures count as not passing, which is **just under** 90%. |
| No open Critical or High bugs | **Not met.** Five High bugs are open. |
| Open Medium/Low bugs documented with a decision | Documented. No fix/defer decision has been recorded yet. |
| CI pipeline green on `main` | Met on the last verified runs (the workflow now also runs the SQL checks and builds the report; that version has not been run on GitHub yet). |

## 6. Risks and limits

- **UI tests run on Chromium only.** Firefox and WebKit were dropped to keep CI short, so browser-specific bugs are not covered.
- **UI tests mostly use one reader per scenario.** They could not see BUG-008 and BUG-009; the API tests, which use several users, found them. A two-reader UI test would close that gap.
- **The UI can hide server problems.** The comment-delete test passed until a reload check was added (BUG-007). Tests that trust what the screen shows should confirm with a reload or the API.
- **Test users are never cleaned up.** Articles are deleted after each test; users accumulate until the database is reset (`docker compose down -v`). The SQL checks run against that shared data.
- **Out of scope** (decided on 2026-11-19): AI/LLM evaluation, accessibility, mobile viewport, JWT expiry and tampering, exploratory sessions, performance. The only security check is the XSS test for markdown article bodies (F17); titles and comments are not covered.

## 7. What went well and what to improve

- Checking the API before blaming the UI found real defects faster than reading test output (BUG-001, 002, 003, 007).
- Writing known bugs as strict expected failures keeps CI honest: nothing is silently skipped, and a fix is noticed automatically.
- Mistakes caught along the way: a UI assertion on an *empty* list passed before data had loaded; an API test file silently failed to be created and the count looked fine until the collected tests were checked. Both were fixed, and the lesson is to verify counts and prove that a check can fail.
- Next: record a fix or defer decision for each open bug, add the two-reader UI test, and run the new CI workflow on GitHub.

## 8. How to reproduce

```sh
# start the stack (see README), then:
scripts/report.sh --open        # API + UI suites and the Allure report
sql/run_checks.sh               # database checks
python3 scripts/gen_test_cases.py   # regenerate docs/test-cases.md
```
