---
name: triage-failure
description: Investigate a failing Playwright or pytest test in this repo and decide whether the test is wrong or the app has a bug, before changing anything. Use this whenever a test fails, goes red in CI, passes when it should fail, or the user asks "why did this fail", "is this a bug", or "check this test", even if they do not say "triage".
---

# Triage a failing test

The expensive mistake is "fixing" a test that was correctly reporting a bug, or reporting a bug that was a flaw in the test. Establish which one it is **before** editing anything.

## Steps

1. **Read the failure.** Run only the failing test (`cd ui-tests && npx playwright test <file> -g "<title>" --reporter=list`, or `api-tests/.venv/bin/python -m pytest <file>::<test>`). For UI failures open `ui-tests/test-results/<test>/error-context.md`: the page snapshot shows what was on screen when it failed.
2. **Check the environment first if many tests fail at once.** `ERR_CONNECTION_REFUSED` / `ECONNREFUSED` means the stack is down or Vite moved off port 8080. Use the `start-stack` skill; this is not a test or app bug.
3. **Reproduce below the UI.** Call the API directly with curl or a short script (put scratch files in the scratchpad directory, not the repo). If the API gives the wrong answer, it is an app bug.
4. **Capture the network** for UI-only problems: a short Playwright script with `page.on('response', ...)` printing method, URL, status and request body. This is how `/profiles/undefined/follow` and the `image: ""` 422 were found.
5. **Rule out test-side causes:**
   - *Passes too early:* an "empty" assertion (`toHaveCount(0)`, "no articles") can succeed while data is still loading. Wait for the response or a visible element first.
   - *Data collisions:* titles must be unique (the slug comes from the title); usernames and emails too.
   - *State leaking between tests*, or selectors matching more than one element (author buttons render twice on the article page).
   - *A test that cannot see the bug:* a UI test that trusts what the screen shows may pass while the server did nothing; confirm with a reload or the API.
6. **Decide and act:**
   - Test bug: fix the test, rerun it, then the whole suite.
   - App bug: hand over to the `log-bug` skill. Do not edit app code under `newsclip/` unless the user asks; the app is the thing under test.
   - Unclear: say what you ruled out and what evidence is missing.
7. **Report briefly:** verdict, the evidence (status codes, snapshot lines), and what you changed.

## Facts about this app that explain odd results

- Deletes are **soft**: rows stay with `record_status = 'deleted'`, and the API returns 404 for them.
- `offset` on article lists is multiplied by `limit` (BUG-001), so later pages come back empty.
- Check `docs/bugs/` before filing: the failure may already be a known bug covered by `test.fail()` / `xfail`.
