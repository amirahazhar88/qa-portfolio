#!/usr/bin/env bash
# Runs the API and UI suites and builds ONE combined Allure report.
# Usage: scripts/report.sh [--open]     (needs the stack up: use the start-stack steps in the README)
# Output: allure-report/index.html
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

rm -rf allure-results allure-report
status=0

echo "== API tests (pytest) =="
(cd api-tests && .venv/bin/python -m pytest -q) || status=1

echo "== UI tests (Playwright) =="
(cd ui-tests && npx playwright test) || status=1

echo "== Allure report =="
ui-tests/node_modules/.bin/allure generate allure-results/api allure-results/ui --config allurerc.mjs --clean || status=1

echo
echo "Report: $root/allure-report/index.html"
[ "${1:-}" = "--open" ] && ui-tests/node_modules/.bin/allure open allure-report --config allurerc.mjs
exit $status
