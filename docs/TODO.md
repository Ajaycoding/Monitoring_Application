# Implementation TODO

Small, AI-friendly increments for the Demo Monitoring Infrastructure, based on [`requirements.md`](./requirements.md).

**Rules**

- Do **one step at a time**.
- Keep the demo **local and minimal** (no cloud deploy).
- Every step must include **security** and **docs**.
- Check boxes when done.

---

## Step 1 — Project initialization and basic UI

- [x] Create minimal Flask layout: `app/`, `templates/`, `static/css/`, `requirements.txt`
- [x] Add base template + simple home/placeholder page with clean CSS
- [x] Add `.gitignore` (`.venv/`, `__pycache__/`, `instance/`, `.env`, IDE files)
- [x] **Security:** Do not commit secrets; read `SECRET_KEY` from env (document a local-only default)
- [x] **Docs:** Root `README.md` — purpose, Python 3.10+, venv, `pip install`, `flask run`
- [x] Verify: app serves basic UI at `http://127.0.0.1:5000`

---

## Step 2 — Sign-in functionality and unit tests

- [x] Add SQLite + minimal `User` model (`username`, `password_hash`)
- [x] Seed default `admin` with a **hashed** password on first run
- [x] Login form (Jinja) + session-based sign-in / sign-out
- [x] Protect non-public routes; redirect unauthenticated users to `/login`
- [x] **Security:** Never store or log plain-text passwords; use Werkzeug (or equivalent) hashing; generic login error
- [x] **Security:** Non-empty `SECRET_KEY` for sessions; session cookie `HttpOnly`
- [x] Unit tests: hash/verify, login success, login failure, logout, protected-route redirect
- [x] **Docs:** Demo credentials + auth notes in `README.md` (warn: local demo only)
- [x] Verify: sign in as `admin`, open a protected page, sign out; `pytest` passes locally

---

## Step 3 — CI/CD with GitHub Actions (minimal)

- [x] Add `.github/workflows/ci.yml` on push/PR to `main` / `master`
- [x] CI steps: set up Python → install `requirements.txt` → run `pytest`
- [x] Pin Python version in CI to match local demo (e.g. 3.10)
- [x] **Security:** Do not print secrets in CI logs; **no deploy jobs** (local demo only)
- [x] **Docs:** Short “CI” section in `README.md`
- [x] Verify: workflow file is valid; tests pass when CI runs

---

## Step 4 — Server inventory (Name + IP/hostname, max ~3)

- [x] Add `Server` model with **`name`** and **`ip_hostname`** (timestamps optional)
- [x] Dashboard list of servers (read-only inventory display)
- [x] Add-server form: **Name** + **IP/hostname**; enforce max **~3** servers
- [x] Reject empty/invalid fields; clear message when over the 3-server cap
- [x] **Security:** Login required; validate/sanitize inputs; prefer CSRF (Flask-WTF) or document as demo limitation
- [x] **Security:** Keep SQLite under `instance/` (gitignored); never serve the DB file
- [x] Unit tests: add server, list servers, reject over-cap / invalid input, auth required
- [x] **Docs:** Document Name + IP/hostname fields, 3-server cap, local persistence
- [x] Verify: add/list up to 3 servers; data survives restart

---

## Step 5 — CPU % metrics (localhost / mock)

- [x] Metrics helper returning **CPU %** (localhost reading or mock for demo)
- [x] Show CPU % on the dashboard next to each server
- [x] Keep metric views **read-only** (no remote shell/SSH actions)
- [x] **Security:** Login required; no shell injection; do not call arbitrary hosts
- [x] Unit tests: CPU value shape/range; dashboard requires auth
- [x] **Docs:** State clearly that collection is **localhost / mock** for this demo
- [x] Verify: dashboard shows CPU % for listed servers

---

## Step 6 — Memory metrics (localhost / mock)

- [x] Extend metrics helper for **memory** (used / free / total)
- [x] Show memory next to CPU on the dashboard (read-only)
- [x] **Security:** Same as Step 5 — auth required; no remote exec; no arbitrary hosts
- [x] Unit tests: memory fields present and sensible; auth still required
- [x] **Docs:** Note memory fields and localhost/mock source
- [x] Verify: dashboard shows CPU % and memory for listed servers

---

## Step 7 — Manual refresh

- [x] Add a **Refresh** control (button and/or page reload) on the dashboard
- [x] Metrics update **only** when the user refreshes (no auto-refresh / WebSockets)
- [x] **Security:** Refresh path stays auth-protected
- [x] Unit/integration test: refresh/dashboard still requires auth
- [x] **Docs:** Note that refresh is manual only
- [x] Verify: clicking Refresh updates displayed CPU and memory

---

## Step 8 — UI polish (read-only demo)

- [x] Improve dashboard layout (server list, CPU, memory, Add form, Refresh, Sign out)
- [x] Empty state when no servers exist
- [x] Friendly messages for validation errors and the 3-server limit
- [x] **Security:** Confirm metrics UI has no write/exec actions beyond inventory add
- [x] **Docs:** Optional short “UI tour” blurb in `README.md` (keep minimal)
- [x] Verify: happy path works for a local demo walkthrough

---

## Step 9 — Final acceptance (PRD checklist)

- [x] Unauthenticated users cannot see the dashboard
- [x] `admin` logs in with hashed-password verification
- [x] Dashboard is read-only for metrics and shows **CPU %** and **memory**
- [x] Admin can add a server with **Name** and **IP/hostname** (up to ~3)
- [x] Metrics update only on manual refresh
- [x] App runs locally with the README steps
- [x] **Security:** Quick pass — no secrets in git; passwords hashed; routes protected
- [x] **Docs:** `README.md` and `docs/requirements.md` match what was built
- [x] Verify: `pytest` green locally; CI workflow still valid

---

## Out of scope (do not implement)

- Multi-user admin / RBAC
- Windows hosts
- SSH/agent collection to remote hosts
- Network, ports, disk, process, uptime metrics
- Auto-refresh / WebSockets
- Alerts, email, tickets
- Long-term history
- Cloud / production deploy
