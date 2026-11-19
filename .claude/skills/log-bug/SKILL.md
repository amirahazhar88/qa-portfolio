---
name: log-bug
description: Write a bug report in docs/bugs/ for a defect found in the newsclip app, link it to an automated test, and update the coverage matrix. Use this whenever a test failure has been confirmed as an app bug rather than a test bug, or the user says "log this bug", "write a bug report", "add this to the bugs", or describes unexpected app behaviour they want recorded, even if they do not mention BUG numbers.
---

# Log a bug

A bug report is only useful if someone else can reproduce it from the page alone, and if the test suite will notice when it is fixed. This skill does both.

## Before writing

Confirm it is an **app** bug, not a test bug (the `triage-failure` skill does this). A report built on a wrong assumption wastes the reader's time. Reproduce it directly (curl or a short script) so the evidence comes from the app, not from a test run.

## Steps

1. **Number it.** `ls docs/bugs/` and take the next `BUG-nnn` (three digits). Check the existing reports for the same defect first; extend that report instead of duplicating.
2. **Write `docs/bugs/BUG-nnn.md`** with this structure (see `docs/bugs/BUG-001.md` as the model):
   - Title: `BUG-nnn: <what is wrong>` (symptom, not guessed cause).
   - Header table: Status (Open), Severity, Priority, Found by, Found on (today), Component (API route or frontend file), Environment.
   - Steps to reproduce, Expected, Actual.
   - **Evidence** as a table of request versus returned versus expected. Real values only.
   - Suspected cause: only after reading the code, and word it as suspected with the file path. If you did not look, say so or omit it.
   - Automation: the exact test(s) that cover it.
3. **Severity** (from `docs/test-plan.md`): Critical = data loss, security, app unusable; High = major feature broken; Medium = works with a workaround; Low = cosmetic. **Priority** P1/P2/P3 follows the feature's priority in the test plan matrix.
4. **Link a test** so the suite stays green while the bug is open and goes red when it is fixed:
   - Playwright: `test.fail(true, 'BUG-nnn: <reason>');` with a comment pointing at the report.
   - pytest: `@pytest.mark.xfail(strict=True, reason="BUG-nnn: <reason>")`.
   Never use `skip`: nobody notices when a skipped test's bug gets fixed.
5. **Update the matrix** in `docs/test-plan.md` (the feature's row) to point at the bug.
6. **Run the affected test** and confirm it reports an expected failure (not a pass, not an error).

Do not commit or push; the user decides when.

## Quality bar

- One defect per report.
- Say what you verified and what you inferred.
- If the UI hides the problem (for example it updates the screen without asking the server), say how it can be seen (a reload, the API).
