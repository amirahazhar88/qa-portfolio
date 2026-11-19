#!/usr/bin/env python3
"""Generates docs/test-cases.md from the real tests, so the document cannot drift from the code.

Usage:  python3 scripts/gen_test_cases.py
Needs:  ui-tests/node_modules (Playwright) and api-tests/.venv (pytest).
"""
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "test-cases.md"

# Which test-plan features (F1..F17, see docs/test-plan.md) a spec file covers.
UI_COVERS = {
    "auth.spec.ts": "F1 Register, F2 Login",
    "session.spec.ts": "F3 Logout and session",
    "route-guards.spec.ts": "F4 Route guards",
    "article.spec.ts": "F6 Create, F7 Edit, F8 Delete",
    "feed.spec.ts": "F9 Feed and pagination, F10 Filters",
    "xss.spec.ts": "F17 Markdown and XSS",
    "settings.spec.ts": "F5 Settings",
    "favorites.spec.ts": "F12 Favorites",
    "follow.spec.ts": "F11 Following feed, F13 Follow, F16 Profiles",
    "comments.spec.ts": "F14 Comments",
}
API_COVERS = {
    "test_users.py": "F1 Register, F2 Login, F5 Settings",
    "test_articles.py": "F6-F10 Articles, feeds and filters, F15 Tags",
    "test_authorization.py": "F4 Auth guards, F7/F8 author-only changes",
    "test_favorites.py": "F12 Favorites",
    "test_profiles.py": "F13 Follow, F16 Profiles",
    "test_comments.py": "F14 Comments",
    "test_health.py": "Service health",
}


def bug_links(text: str) -> str:
    bugs = sorted(set(re.findall(r"BUG-\d{3}", text)))
    return ", ".join(f"[{b}](bugs/{b}.md)" for b in bugs)


def ui_tests():
    out = subprocess.run(
        ["npx", "playwright", "test", "--list", "--reporter=json"],
        cwd=ROOT / "ui-tests", capture_output=True, text=True, check=True,
    ).stdout
    rows = []

    def walk(suite, path=()):
        for spec in suite.get("specs", []):
            rows.append((path, spec))
        for child in suite.get("suites", []):
            walk(child, path + (child["title"],))

    for suite in json.loads(out)["suites"]:
        walk(suite)

    by_file = {}
    for path, spec in rows:
        by_file.setdefault(spec["file"], []).append((spec["line"], path, spec))
    result = {}
    for file, items in by_file.items():
        items.sort(key=lambda i: i[0])
        source = (ROOT / "ui-tests" / "tests" / file).read_text().splitlines()
        fails = [(n + 1, bug_links(line)) for n, line in enumerate(source) if "test.fail(true" in line]
        lines = [i[0] for i in items]
        entries = []
        for idx, (line, path, spec) in enumerate(items):
            upper = lines[idx + 1] if idx + 1 < len(lines) else 10**9
            bugs = ", ".join(b for n, b in fails if line <= n < upper and b)
            tags = " ".join("@" + t for t in spec.get("tags", []))
            entries.append((path[-1] if path else "", spec["title"], tags, bugs))
        result[file] = entries
    return result


COLLECTOR = r"""
import json, sys, pytest
class C:
    def pytest_collection_modifyitems(self, items):
        data = []
        for it in items:
            x = it.get_closest_marker("xfail")
            data.append({
                "file": it.path.name,
                "group": it.cls.__name__ if it.cls else "",
                "name": it.name,
                "smoke": it.get_closest_marker("smoke") is not None,
                "xfail": (x.kwargs.get("reason", "") if x else ""),
            })
        sys.stdout.write("@@JSON@@" + json.dumps(data) + "@@END@@")
pytest.main(["--collect-only", "-q", "-p", "no:cacheprovider", "-o", "addopts="], plugins=[C()])
"""


def api_tests():
    proc = subprocess.run(
        [str(ROOT / "api-tests" / ".venv" / "bin" / "python"), "-c", COLLECTOR],
        cwd=ROOT / "api-tests", capture_output=True, text=True, check=True,
    )
    data = json.loads(proc.stdout.split("@@JSON@@")[1].split("@@END@@")[0])
    result = {}
    for d in data:
        result.setdefault(d["file"], []).append(d)
    return result


def humanize(name: str) -> str:
    base, _, param = name.partition("[")
    text = base.removeprefix("test_").replace("_", " ")
    text = text[0].upper() + text[1:]
    return f"{text} ({param.rstrip(']')})" if param else text


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def main():
    ui, api = ui_tests(), api_tests()
    ui_total = sum(len(v) for v in ui.values())
    api_total = sum(len(v) for v in api.values())
    known = sum(1 for v in ui.values() for e in v if e[3]) + sum(1 for v in api.values() for e in v if e["xfail"])

    lines = [
        "# newsclip test cases",
        "",
        "> **Generated** by `python3 scripts/gen_test_cases.py` from the real tests. Do not edit by hand; change the tests and regenerate.",
        "",
        f"Generated on {date.today().isoformat()}: **{ui_total + api_total} automated test cases** "
        f"({ui_total} UI, {api_total} API), of which **{known}** cover a known defect and are expected to fail until it is fixed. "
        "SQL checks are listed in [`sql/README.md`](../sql/README.md).",
        "",
        "How to read it: *Covers* uses the feature IDs (F1 to F17) of the [coverage matrix](test-plan.md). "
        "*Known defect* links to the bug report; those tests are written to fail until the bug is fixed "
        "(`test.fail()` in Playwright, `xfail(strict=True)` in pytest).",
        "",
        "## UI tests (Playwright, `ui-tests/tests/`)",
    ]
    n = 0
    for file in sorted(ui):
        lines += ["", f"### `{file}`", f"Covers: {UI_COVERS.get(file, '')}", "",
                  "| ID | Group | Test case | Tags | Known defect |", "|---|---|---|---|---|"]
        for group, title, tags, bugs in ui[file]:
            n += 1
            lines.append(f"| UI-{n:03d} | {esc(group)} | {esc(title)} | {tags} | {bugs} |")
    lines += ["", "## API tests (pytest, `api-tests/tests/`)"]
    n = 0
    for file in sorted(api):
        lines += ["", f"### `{file}`", f"Covers: {API_COVERS.get(file, '')}", "",
                  "| ID | Group | Test case | Tags | Known defect |", "|---|---|---|---|---|"]
        for d in api[file]:
            n += 1
            group = re.sub(r"(?<!^)(?=[A-Z])", " ", d["group"].removeprefix("Test")) if d["group"] else ""
            lines.append(
                f"| API-{n:03d} | {esc(group)} | {esc(humanize(d['name']))} | {'@smoke' if d['smoke'] else ''} | {bug_links(d['xfail'])} |"
            )
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {ui_total} UI + {api_total} API, {known} known-defect tests")


if __name__ == "__main__":
    main()
