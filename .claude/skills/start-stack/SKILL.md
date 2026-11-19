---
name: start-stack
description: Start (or repair) the local newsclip test stack - Docker Desktop, the API and MySQL on :3100, and the Vite frontend on :8080 - and confirm both respond. Use this whenever the user asks to start, run, restart or check the app, whenever tests fail with ERR_CONNECTION_REFUSED / ECONNREFUSED, after a reboot or branch switch, or before running any Playwright or pytest suite, even if they do not say "stack".
---

# Start the newsclip stack

The UI tests (`ui-tests/`) and API tests (`api-tests/`) need two things running locally:

| Part | URL | How it runs |
|---|---|---|
| API + MySQL | `http://localhost:3100/api` | Docker Compose in `newsclip/api` |
| Frontend | `http://localhost:8080` | Vite dev server in `newsclip/web` |

Check what is already up first. Starting things that are running wastes time and can hide the real problem.

## Steps

1. **Probe** both URLs: `curl -s -o /dev/null -w "%{http_code}" localhost:3100/api/health-check` and `localhost:8080`. If both return 200, report that and stop.
2. **Docker.** If `docker info` fails, run `open -a Docker` and poll `docker info` (up to about 90 s). Containers are stopped after a Docker restart, which is the usual reason the API is down.
3. **API.** `cd newsclip/api && docker compose up -d`. Add `--build` only if the code changed. The compose file has a MySQL healthcheck, so the migration waits for the database; just poll `/api/health-check` until 200 (up to about 2 min).
4. **Frontend.** Make sure `newsclip/web/.env.local` exists (copy `.env.example`; it sets `VITE_API_URL=http://localhost:3100/api`), and run `npm install` if `node_modules` is missing. Then start it in the background: `nohup npm run serve > /tmp/vite-newsclip.log 2>&1 &`.
5. **Verify** `localhost:8080` returns 200 **and** the log says port 8080 (see the port trap below). Report both URLs and anything you had to fix.

## Traps seen in this project

- **Vite jumps to port 5173.** Switching git branches rewrites `vite.config.js`; Vite restarts while the file is being replaced, reads defaults, and moves to 5173. Tests then fail with `ERR_CONNECTION_REFUSED` on 8080. Fix: kill the Vite process for this repo and run step 4 again. Do not kill unrelated node processes.
- **Without `VITE_API_URL`** the frontend silently calls the public `api.realworld.show`. Always check `.env.local`.
- **`docker compose down -v` deletes the database** (all test users). Never run it unless the user asks for a reset.
- If the API container is `Exited`, read `docker compose logs` before restarting repeatedly.
