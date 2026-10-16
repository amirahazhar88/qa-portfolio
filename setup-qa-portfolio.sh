#!/usr/bin/env bash
# Run this from the ROOT of your cloned qa-portfolio repo.
# Safe to re-run: it will not duplicate lines or overwrite existing folders.

set -e

if [ ! -d ".git" ]; then
  echo "Error: run this inside your qa-portfolio folder (the one containing .git)."
  exit 1
fi

# 1. Folder structure (with .gitkeep so Git tracks empty folders)
for dir in docs ui-tests api-tests ai-tests sql .github/workflows; do
  mkdir -p "$dir"
  [ -e "$dir/.gitkeep" ] || touch "$dir/.gitkeep"
done

# 2. .gitignore additions (only if not already present)
touch .gitignore
add_ignore() {
  grep -qxF "$1" .gitignore || echo "$1" >> .gitignore
}
if ! grep -qxF "# Python" .gitignore; then
  printf "\n# Python\n" >> .gitignore
fi
add_ignore ".venv/"
add_ignore "__pycache__/"
add_ignore "*.pyc"
add_ignore ".pytest_cache/"
if ! grep -qxF "# Secrets and test output" .gitignore; then
  printf "\n# Secrets and test output\n" >> .gitignore
fi
add_ignore ".env"
add_ignore "playwright-report/"
add_ignore "test-results/"
add_ignore "node_modules/"

# 3. .env.example (safe to commit, no real values)
if [ ! -e ".env.example" ]; then
  cat > .env.example <<'EOF'
BASE_URL=
API_URL=
API_TOKEN=
LLM_API_KEY=
EOF
fi

# 4. README skeleton (only if README is still the short default)
if [ ! -e "README.md" ] || [ "$(wc -l < README.md)" -lt 8 ]; then
  cat > README.md <<'EOF'
# qa-portfolio

Test automation and AI/LLM evaluation project.

## What this project covers
- UI automation (Playwright)
- API testing (Postman, pytest)
- SQL data checks
- CI with GitHub Actions
- AI/LLM evaluation with a rubric

## Application under test
(Add after choosing the app)

## Project structure
- `docs/` test plan, test cases, bug reports
- `ui-tests/` Playwright tests
- `api-tests/` Postman collection and pytest
- `ai-tests/` LLM eval set and runner
- `sql/` data integrity queries

## How to run
(Add as you build)

## AI-assisted workflow
(Add in Week 1)
EOF
else
  echo "README.md already has content, left unchanged."
fi

echo ""
echo "Done. Next:"
echo "  git checkout -b setup-structure"
echo "  git add ."
echo "  git commit -m \"Add project structure and README skeleton\""
echo "  git push origin setup-structure"
