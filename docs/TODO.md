# Implementation TODO

Demo Monitoring Infrastructure — small, AI-friendly increments based on [`requirements.md`](./requirements.md).

**How to use:** Complete steps in order. Each step should leave the app runnable (or clearly note if not). Check boxes as you finish. Keep the demo local and minimal.

---

## Step 0 — Project initialization and basic UI

- [x] Create minimal Flask app layout (`app/`, `templates/`, `static/css/`, `requirements.txt`)
- [x] Add a simple home/placeholder page with base layout and attractive but minimal CSS
- [x] Add `.gitignore` (venv, `__pycache__`, `instance/`, `.env`, IDE files)
- [x] **Security:** Do not commit secrets; use a placeholder `SECRET_KEY` from env with a documented local default
- [x] **Docs:** Add root `README.md` with project purpose, Python version, how to create a venv, install deps, and run the app
- [x] Verify: `flask run` (or `python -m flask run`) serves the basic UI locally

---

## Step 1 — Sign-in functionality and unit tests

- [x] Add SQLite + minimal `User` model (`username`, `password_hash`)
- [x] Seed default `admin` user with a **hashed** password on first run
- [x] Implement login form (Jinja) + session-based sign-in / sign-out
- [x] Protect non-public routes so unauthenticated users are redirected to login
- [x] **Security:** Never store or log plain-text passwords; use Werkzeug (or equivalent) password hashing; generic login error message
- [x] **Security:** Set a non-empty `SECRET_KEY` for sessions; keep session cookie `HttpOnly`
- [x] Add unit tests for: password hashing/verify, successful login, failed login, logout, protected-route redirect
- [x] **Docs:** Document default demo credentials and auth behavior in `README.md` (warn: demo only)
- [x] Verify: can sign in as `admin`, access a protected page, sign out; tests pass locally

---

## Step 2 — CI/CD with GitHub Actions (minimal)

- [ ] Add `.github/workflows/ci.yml` to run on push/PR to main branches
- [ ] CI jobs: install Python deps, run unit tests (and optionally lint if already configured)
- [ ] Pin or document Python version used in CI to match local demo
- [ ] **Security:** CI must not print secrets; use GitHub Actions defaults only (no production deploy for this demo)
- [ ] **Docs:** Short “CI” section in `README.md` describing what the workflow runs
- [ ] Verify: workflow file is valid; tests pass in CI when repo is on GitHub

---

## Step 3 — Server inventory (SQLite)

- [ ] Add `Server` model (`name`, `host`, optional `notes`, `created_at`)
- [ ] Server list page (read-only table/cards)
- [ ] Add-server form (POST); validate required fields
- [ ] Delete server with a simple confirmation
- [ ] Prefer blocking exact duplicate `host` values with a clear message
- [ ] **Security:** Require login for all inventory routes; validate/sanitize form input; use CSRF protection if easy (e.g. Flask-WTF), otherwise document as a known demo limitation
- [ ] **Security:** Do not expose the SQLite file via static/media routes; keep DB under `instance/` (gitignored)
- [ ] Unit tests: create server, list servers, reject invalid/duplicate host, delete server, auth required
- [ ] **Docs:** Document inventory fields and how data persists across restarts
- [ ] Verify: add/list/delete servers; data survives app restart

---

## Step 4 — Mock metrics (CPU, memory, network, ports)

- [ ] Add `metrics` helper that returns plausible mock values per server id/host
- [ ] Vary mock values slightly over time so refresh feels live
- [ ] Server detail page showing CPU %, memory used/total/%, network RX/TX, listening ports list
- [ ] Keep metric views **read-only** (no remote actions)
- [ ] **Security:** Authorize access (login required); ensure server id cannot leak data beyond mock payload; no shell/network calls to real hosts
- [ ] Unit tests: metrics shape/ranges; detail page requires auth; 404 for unknown server
- [ ] **Docs:** State clearly that metrics are **mocked** for the demo
- [ ] Verify: detail page shows all four metric areas

---

## Step 5 — Auto-refresh every 5 seconds

- [ ] Auto-refresh server detail (and optionally dashboard summary) every **5 seconds**
- [ ] Prefer the simplest approach (meta-refresh or small fetch to a JSON/HTML partial)
- [ ] Show a non-blocking message if a refresh fails
- [ ] Make refresh interval configurable (default `5`) via config/env
- [ ] **Security:** Refresh endpoints remain auth-protected; do not widen CORS or disable sessions for convenience
- [ ] Unit/integration test: refresh endpoint requires auth and returns expected payload
- [ ] **Docs:** Document refresh interval and how to change it
- [ ] Verify: metrics visibly update about every 5 seconds in the browser

---

## Step 6 — UI polish (still Jinja + CSS only)

- [ ] Improve layout consistency (nav with sign-out, empty states, flash messages)
- [ ] Clear visual hierarchy for CPU / memory / network / ports
- [ ] Basic responsive layout for laptop screens (no mobile app)
- [ ] **Security:** Avoid leaking internal errors in UI; keep flash messages generic where appropriate
- [ ] **Docs:** Add a short screenshots or “pages overview” section to `README.md`
- [ ] Verify: walk through login → list → add → detail → logout feels demo-ready

---

## Step 7 — Final demo hardening and docs pass

- [ ] Confirm `.env.example` (or README config table) lists `SECRET_KEY`, DB path, refresh interval — no real secrets committed
- [ ] Confirm `.gitignore` covers `instance/`, `.env`, venv, caches
- [ ] Run full local test suite; fix any failures
- [ ] Confirm GitHub Actions CI still passes
- [ ] **Security checklist:** hashed admin password; protected routes; no plain secrets in git; SQLite not publicly served; metrics remain mock/read-only
- [ ] **Docs:** Final README pass — setup, run, test, CI, default login, out-of-scope list linking to PRD
- [ ] Verify acceptance criteria from `docs/requirements.md` §9

---

## Explicitly out of scope (do not implement)

- [ ] ~~Alerts / notifications~~
- [ ] ~~Multi-user roles (L1/L2/L3 permissions)~~
- [ ] ~~Windows hosts~~
- [ ] ~~Long-term historical metrics storage~~
- [ ] ~~Mobile app~~
- [ ] ~~Real SSH/agent metric collection~~
- [ ] ~~Production deploy / cloud hosting~~

---

## Progress tracker

| Step | Focus | Status |
| --- | --- | --- |
| 0 | Project init + basic UI | Done |
| 1 | Sign-in + unit tests | Done |
| 2 | GitHub Actions CI | Not started |
| 3 | Server inventory (SQLite) | Not started |
| 4 | Mock metrics | Not started |
| 5 | 5s auto-refresh | Not started |
| 6 | UI polish | Not started |
| 7 | Final hardening + docs | Not started |
