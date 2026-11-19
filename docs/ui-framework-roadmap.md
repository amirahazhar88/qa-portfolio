# UI automation framework: 8-step build guide

A reference for how the Playwright framework in `ui-tests/` is built, step by step. Each step builds on the one before it.

**Stack:** Playwright + TypeScript, testing **newsclip** (`newsclip/`).
**Related:** [test-plan.md](test-plan.md) says *what* to test. This guide says *how the framework is built*.

## Status

| # | Step | Status |
|---|------|--------|
| 1 | Reliable test target | ✅ Done |
| 2 | Page Object Model | ✅ Done |
| 3 | Fixtures | ✅ Done (not yet committed) |
| 4 | API-based setup | ✅ Done (not yet committed) |
| 5 | Test data factory | ✅ Done (not yet committed) |
| 6 | Feature coverage | 🟡 P1 and P2 done (not yet committed); P3 (tags list, profile polish) remaining. 4 bugs logged in `docs/bugs/` |
| 7 | CI | 🟡 Workflow moved to root, not yet proven green |
| 8 | Docs | 🟡 Test plan drafted, README partly done |

---

## Step 1: Reliable test target

**Goal:** Tests run against an app you control, not a shared public one.

**What we did**
- Run the API (Node + MySQL) with Docker Compose on `:3100` and the Vue frontend on `:8080`.
- Point the frontend at the local API with `VITE_API_URL` in `newsclip/web/.env.local`.
- Document the start-up steps in the README.

**Why:** A shared public API can be down, slow, or full of other people's data. Flaky target means flaky tests, and you can't tell a bug from bad luck.

**Done when:** A cold start (`docker compose up`) works and the tests pass against it.

---

## Step 2: Page Object Model (POM)

**Goal:** One place that knows *how to find and use* each page.

**Files:** `ui-tests/pages/LoginPage.ts`, `RegisterPage.ts`, `NavBar.ts`

**Rules**
- A page object holds **locators**, **actions** (`login()`, `register()`), and **navigation** (`goto()`).
- **Assertions stay in the spec**, so a failing test shows what was being verified.
- No test data and no test logic in page objects.

**Why:** When the UI changes (a placeholder is renamed), you fix one file, not every test.

**Done when:** Specs contain no raw selectors.

---

## Step 3: Fixtures

**Goal:** Tests *ask for* what they need and Playwright sets it up.

**Files:** `ui-tests/fixtures/index.ts`

```ts
export const test = base.extend<Pages>({
  loginPage: async ({ page }, use) => { await use(new LoginPage(page)); },
  ...
});
```

In a spec, import `test` and `expect` from `../fixtures` (not `@playwright/test`), then:

```ts
test('...', async ({ loginPage, nav }) => { ... });
```

**Why:** No more `new LoginPage(page)` in every test. Later, the same mechanism provides things like a logged-in user or a test article, and cleans up afterwards.

**Done when:** All specs get their page objects from fixtures.

---

## Step 4: API-based setup

**Goal:** Create preconditions through the API, not by clicking through the UI.

**Files:** `helpers/api.ts`, new fixtures in `fixtures/index.ts`, `tests/session.spec.ts`, root `.env`

**What we did**
- Installed `dotenv`. `playwright.config.ts` loads the repo-root `.env` (`BASE_URL`, `API_URL`). The committed template is `.env.example`; the real `.env` is git-ignored.
- `ApiClient` (`helpers/api.ts`) calls the REST API: `registerUser()` and `login()`.
- New fixtures: `api` (the client), `user` (a fresh user created via the API) and `authedPage` (a browser page already signed in as that user).
- How `authedPage` works: the app keeps its JWT in `localStorage` under `jwtToken`, so the fixture plants the token with `page.addInitScript()` before any page script runs.
- Only the login/register tests go through the forms.

**Design choice:** one new user per test (one fast HTTP call) keeps tests fully isolated. Playwright's `storageState` (log in once, reuse for the whole run) is the alternative for a single shared account. It's faster but shares state, so we use it only if setup time becomes a problem.

**Why:** Faster and far less flaky. If the login UI breaks, only the login tests fail.

**Done when:** A test can start already logged in without touching the login page. ✅

---

## Step 5: Test data factory

**Goal:** Unique, independent data from one place, with cleanup.

**Files:** `test-data/factory.ts`, `pages/ArticlePage.ts`, `tests/article.spec.ts`, extra methods in `helpers/api.ts`, new fixture in `fixtures/index.ts`

**What we did**
- `buildUser()` and `buildArticle()` create unique data (timestamp + random suffix). Specs no longer build usernames or titles by hand. Pass overrides when a test needs a specific value: `buildArticle({ title: 'x' })`.
- Titles must be unique: the API builds the article **slug from the title**, so duplicate titles collide.
- `ApiClient.createArticle()` and `deleteArticle()` (Bearer token).
- New `article` fixture: creates an article as `user` via the API, hands it to the test, then **deletes it after the test** (the code after `use()`).

**Good to know:** the app uses **soft delete**. A deleted article stays in MySQL with `record_status = 'deleted'`, but the API returns 404 for it. SQL checks (step in the test plan) must filter on `record_status = 'active'`. Users are not cleaned up. Reset the local database with `docker compose down -v` when it gets full.

**Why:** Tests that share data break each other, especially when run in parallel.

**Done when:** No spec builds usernames or article titles by hand, and tests leave no live articles behind. ✅

---

## Step 6: Feature coverage

**Goal:** Cover the features in the [test plan](test-plan.md) coverage matrix, highest priority first.

| Priority | Features |
|---|---|
| P1 | Logout / session, route guards, create / edit / delete article, global feed, XSS sanitisation |
| P2 | Favorites, follows, comments, filters, following feed, settings |
| P3 | Tags, profile pages |

**Also:** tag tests (`@smoke`, `@regression`) so subsets can run (`npx playwright test --grep @smoke`).

**Done when:** The matrix in the test plan is updated to match what's automated.

---

## Step 7: CI (GitHub Actions)

**Goal:** Tests run automatically and the project is proven to build from scratch.

**File:** `.github/workflows/playwright.yml` (must be at the repo **root**; GitHub ignores workflows elsewhere)

**It must:** start the API, start the frontend, wait until both respond, install dependencies and browsers, run the tests, and upload the HTML report.

**Runs on:** a push to `main`, or a pull request targeting `main`. Every run starts on a clean machine, so installs happen every time.

**Done when:** The workflow is green on a pull request.

---

## Step 8: Documentation

**Goal:** A stranger can understand and run the project in minutes.

**What**
- README: what the project is, how to run each part, how to run the tests.
- `docs/test-plan.md`, `docs/test-cases.md`, `docs/bugs/`, `docs/test-summary.md`.
- Keep the coverage matrix and this guide's status table current.

**Done when:** Someone can clone the repo, follow the README, and see green tests.

---

## Security notes

Habits to keep while building the framework.

| Risk | Habit |
|---|---|
| **Secrets in git** | Real tokens and passwords go only in `.env` (git-ignored) or CI secrets. `.env.example` holds empty or local-only values. |
| **Hardcoded test password** | `Passw0rd!123` is fine for throwaway local users. For any shared environment, read credentials from `.env` or CI secrets. |
| **Wrong target** | Never point `BASE_URL` / `API_URL` at production or a shared environment. Tests create junk users and data. |
| **Tokens in reports and traces** | Playwright traces and HTML reports can record request bodies and storage (tokens, passwords). Don't publish reports from real environments; keep this repo private while the reports are CI artifacts. |
| **Dev secrets in `docker-compose.yml`** | The JWT secret and database passwords are public dev values from the upstream project. Local only; never reuse them elsewhere. |

**Why injecting a token is safe here:** `authedPage` plants the JWT in `localStorage` (key `jwtToken`), exactly where the app puts it after a real login. No security check is bypassed. The API still validates the token like any other request, and all users are throwaway accounts in a local Docker database.

**An app-level risk to test (not caused by the framework):** a JWT in `localStorage` can be stolen if the app has an XSS bug. This is test-plan feature **F17** (XSS sanitisation, P1) and is covered in step 6.

---

## Quick reference

```sh
# start the app
cd newsclip/api && docker compose up -d
cd newsclip/web && npm run serve

# run the tests
cd ui-tests
npx playwright test                          # Chromium (the only configured browser)
npx playwright test --ui                     # interactive mode
npx playwright show-report                   # open the last HTML report
```

If every test fails with `ERR_CONNECTION_REFUSED`, the frontend isn't running on `:8080`. Check `npm run serve`.
