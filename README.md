# qa-portfolio

Test automation project: UI (Playwright), API (pytest) and SQL checks, with CI and an Allure report.

## What this project covers
- UI automation (Playwright)
- API testing (pytest + requests)
- SQL data integrity checks
- CI with GitHub Actions
- Allure test report

## Application under test
**newsclip**, a news/blogging app (articles, comments, favorites, follows, tags). It lives in this repo under [`newsclip/`](newsclip), adapted from the MIT-licensed [RealWorld](https://github.com/gothinkster/realworld) example apps:

| Part | Folder | Stack | Local URL |
|------|--------|-------|-----------|
| Frontend | [`newsclip/web`](newsclip/web) | Vue 3, Pinia, Vite | http://localhost:8080 |
| API | [`newsclip/api`](newsclip/api) | Node/Express, MySQL, Docker Compose | http://localhost:3100/api |

## Project structure
- `docs/` test plan, test cases, bug reports
- `ui-tests/` Playwright tests
- `api-tests/` pytest + requests
- `sql/` data integrity queries

## How to run
1. **API** (needs Docker):
   ```sh
   cd newsclip/api && docker compose up -d --build
   ```
2. **Frontend:**
   ```sh
   cd newsclip/web
   cp .env.example .env.local   # points the app at http://localhost:3100/api
   npm install && npm run serve
   ```
3. **API tests** (pytest):
   ```sh
   cd api-tests
   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
   .venv/bin/python -m pytest
   ```
4. **UI tests** (Playwright):
   ```sh
   cd ui-tests
   npm ci && npx playwright install chromium
   npm test                                  # Chromium (the only configured browser)
   BASE_URL=http://localhost:8080 npm test
   npm run test:headed                       # watch the browser; also test:ui and report
   ```
5. **SQL checks** (needs the Docker stack):
   ```sh
   sql/run_checks.sh
   ```

## Test report
One combined [Allure](https://allurereport.org/) report for the API and UI suites:

```sh
scripts/report.sh --open        # runs both suites, writes allure-report/index.html
```
In CI the report is attached to every run as the `allure-report` artifact, and published to GitHub Pages for pushes to `main` (run history and trends are kept between runs). Publishing needs *Settings > Pages > Source: GitHub Actions*.

## Documentation
| Document | What it is |
|---|---|
| [docs/test-plan.md](docs/test-plan.md) | Scope, approach, risks, exit criteria, feature coverage matrix |
| [docs/test-cases.md](docs/test-cases.md) | Every automated test case (generated from the code) |
| [docs/test-summary.md](docs/test-summary.md) | Results, defects, exit-criteria verdict |
| [docs/bugs/](docs/bugs) | Nine defect reports with evidence |
| [docs/ui-framework-roadmap.md](docs/ui-framework-roadmap.md) | How the UI framework was built, step by step |

## AI-assisted workflow
This project was built with Claude Code as a pairing partner, working like a senior colleague: I set the goals and made the decisions, and the assistant wrote code, explained the reasoning, and challenged results.

**What I decided:** the application to test and its rebrand, the tool choices (Playwright, pytest, Allure), which scope to cut (AI evaluation, accessibility, exploratory testing, extra browsers), when to commit, push and merge, and when the repo goes public.

**How the assistant was used:** drafting page objects, fixtures and specs; probing the API to learn real behaviour before writing assertions; investigating failures; drafting bug reports and documents; and reviewing diffs before they were committed.

**Rules that kept the output trustworthy:**
- Reproduce a failure below the UI (curl, API calls) before calling it an app bug or changing a test.
- Prove a check can fail (inject a bad row, or run the test without the fix) before trusting a pass.
- Known defects are written as strict expected failures, so the suite stays honest and notices when a bug is fixed.
- Nothing is committed, pushed or merged unless I ask for it.
- Verify counts and file lists after generated edits. A silent failure once left a whole test file uncreated; it was caught by checking the collected test count.

**Reusable workflows** are saved as project skills in [`.claude/skills/`](.claude/skills): `start-stack`, `log-bug` and `triage-failure`.

