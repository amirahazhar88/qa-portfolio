#!/usr/bin/env bash
# Runs every sql/checks/*.sql against the newsclip MySQL container.
# A check is a SELECT that returns the *offending* rows: no rows = pass.
# "-- known: BUG-nnn" marks a defect we expect to find (XFAIL). If such a check
# starts passing, that is reported as XPASS and fails the run, so the marker gets removed.
#
# Usage: sql/run_checks.sh            (needs the Docker stack up)
set -u

CONTAINER="${MYSQL_CONTAINER:-newsclip-mysql}"
DB_USER="${MYSQL_USER:-conduit}"
DB_NAME="${MYSQL_DATABASE:-conduit-local}"
# Public dev defaults from newsclip/api/docker-compose.yml (local test stack only).
DB_PASSWORD="${MYSQL_PASSWORD:-how-do-you-turn-this-on-twice}"

dir="$(cd "$(dirname "$0")" && pwd)/checks"
pass=0; fail=0; xfail=0; xpass=0; errors=0

for file in "$dir"/*.sql; do
  name="$(sed -n 's/^-- name: //p' "$file" | head -1)"
  known="$(sed -n 's/^-- known: //p' "$file" | head -1)"
  out="$(docker exec -i -e MYSQL_PWD="$DB_PASSWORD" "$CONTAINER" mysql -u"$DB_USER" "$DB_NAME" -B < "$file" 2>&1)"
  status=$?
  if [ $status -ne 0 ]; then
    printf 'ERROR  %s\n       %s\n' "$name" "$out"; errors=$((errors+1)); continue
  fi
  rows=$(printf '%s\n' "$out" | sed '1d' | grep -c .)   # first line is the column header
  if [ "$rows" -eq 0 ]; then
    if [ -n "$known" ]; then printf 'XPASS  %s   (%s looks fixed: remove the "-- known" line)\n' "$name" "$known"; xpass=$((xpass+1))
    else printf 'PASS   %s\n' "$name"; pass=$((pass+1)); fi
  else
    if [ -n "$known" ]; then label="XFAIL"; xfail=$((xfail+1)); else label="FAIL "; fail=$((fail+1)); fi
    printf '%s  %s   [%s offending row(s)%s]\n' "$label" "$name" "$rows" "${known:+, known: $known}"
    printf '%s\n' "$out" | head -4 | sed 's/^/         /'
  fi
done

printf '\n%s passed, %s failed, %s expected failures, %s unexpected passes, %s errors\n' "$pass" "$fail" "$xfail" "$xpass" "$errors"
[ "$fail" -eq 0 ] && [ "$xpass" -eq 0 ] && [ "$errors" -eq 0 ]
