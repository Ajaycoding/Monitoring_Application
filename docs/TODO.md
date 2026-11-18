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

- [ ] Add SQLite + minimal `User` model (`username`, `password_hash`)
- [ ] Seed default `admin` with a **hashed** password on first run
- [ ] Login form (Jinja) + session-based sign-in / sign-out
- [ ] Protect non-public routes; redirect unauthenticated users to `/login`
- [ ] **Security:** Never store or log plain-text passwords; use Werkzeug (or equivalent) hashing; generic login error
- [ ] **Security:** Non-empty `SECRET_KEY` for sessions; session cookie `HttpOnly`
- [ ] Unit tests: hash/verify, login success, login failure, logout, protected-route redirect
- [ ] **Docs:** Demo credentials + auth notes in `README.md` (warn: local demo only)
- [ ] Verify: sign in as `admin`, open a protected page, sign out; `pytest` passes locally

---

## Step 3 — CI/CD with GitHub Actions (minimal)

- [ ] Add `.github/workflows/ci.yml` on push/PR to `main` / `master`
- [ ] CI steps: set up Python → install `requirements.txt` → run `pytest`
- [ ] Pin Python version in CI to match local demo (e.g. 3.10)
- [ ] **Security:** Do not print secrets in CI logs; **no deploy jobs** (local demo only)
- [ ] **Docs:** Short “CI” section in `README.md`
- [ ] Verify: workflow file is valid; tests pass when CI runs

---

## Step 4 — Server inventory (Name + IP/hostname, max ~3)

- [ ] Add `Server` model with **`name`** and **`ip_hostname`** (timestamps optional)
- [ ] Dashboard list of servers (read-only inventory display)
- [ ] Add-server form: **Name** + **IP/hostname**; enforce max **~3** servers
- [ ] Reject empty/invalid fields; clear message when over the 3-server cap
- [ ] **Security:** Login required; validate/sanitize inputs; prefer CSRF (Flask-WTF) or document as demo limitation
- [ ] **Security:** Keep SQLite under `instance/` (gitignored); never serve the DB file
- [ ] Unit tests: add server, list servers, reject over-cap / invalid input, auth required
- [ ] **Docs:** Document Name + IP/hostname fields, 3-server cap, local persistence
- [ ] Verify: add/list up to 3 servers; data survives restart

---

## Step 5 — CPU % metrics (localhost / mock)

- [ ] Metrics helper returning **CPU %** (localhost reading or mock for demo)
- [ ] Show CPU % on the dashboard next to each server
- [ ] Keep metric views **read-only** (no remote shell/SSH actions)
- [ ] **Security:** Login required; no shell injection; do not call arbitrary hosts
- [ ] Unit tests: CPU value shape/range; dashboard requires auth
- [ ] **Docs:** State clearly that collection is **localhost / mock** for this demo
- [ ] Verify: dashboard shows CPU % for listed servers

---

## Step 6 — Memory metrics (localhost / mock)

- [ ] Extend metrics helper for **memory** (used / free / total)
- [ ] Show memory next to CPU on the dashboard (read-only)
- [ ] **Security:** Same as Step 5 — auth required; no remote exec; no arbitrary hosts
- [ ] Unit tests: memory fields present and sensible; auth still required
- [ ] **Docs:** Note memory fields and localhost/mock source
- [ ] Verify: dashboard shows CPU % and memory for listed servers

---

## Step 7 — Manual refresh

- [ ] Add a **Refresh** control (button and/or page reload) on the dashboard
- [ ] Metrics update **only** when the user refreshes (no auto-refresh / WebSockets)
- [ ] **Security:** Refresh path stays auth-protected
- [ ] Unit/integration test: refresh/dashboard still requires auth
- [ ] **Docs:** Note that refresh is manual only
- [ ] Verify: clicking Refresh updates displayed CPU and memory

---

## Step 8 — UI polish (read-only demo)

- [ ] Improve dashboard layout (server list, CPU, memory, Add form, Refresh, Sign out)
- [ ] Empty state when no servers exist
- [ ] Friendly messages for validation errors and the 3-server limit
- [ ] **Security:** Confirm metrics UI has no write/exec actions beyond inventory add
- [ ] **Docs:** Optional short “UI tour” blurb in `README.md` (keep minimal)
- [ ] Verify: happy path works for a local demo walkthrough

---

## Step 9 — Final acceptance (PRD checklist)

- [ ] Unauthenticated users cannot see the dashboard
- [ ] `admin` logs in with hashed-password verification
- [ ] Dashboard is read-only for metrics and shows **CPU %** and **memory**
- [ ] Admin can add a server with **Name** and **IP/hostname** (up to ~3)
- [ ] Metrics update only on manual refresh
- [ ] App runs locally with the README steps
- [ ] **Security:** Quick pass — no secrets in git; passwords hashed; routes protected
- [ ] **Docs:** `README.md` and `docs/requirements.md` match what was built
- [ ] Verify: `pytest` green locally; CI workflow still valid

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
