# Product Requirements Document (PRD)
## Demo Monitoring Infrastructure — Linux Servers

| Field | Value |
| --- | --- |
| **Product** | Demo Monitoring Infrastructure |
| **Version** | 1.0 (Demo) |
| **Status** | Agreed (all option A) |
| **Audience** | Internal L1 / L2 / L3 infrastructure and application teams |
| **Deployment** | Local only (machine where Cursor is running) |
| **Stack** | Python, Flask, Jinja templates, CSS |

---

## 1. Summary

Local demo web app that shows **read-only** Linux server **CPU %** and **memory** in a simple UI so teams do not need to SSH in for a quick check.

**Agreed scope (all option A):**

| Topic | Choice |
| --- | --- |
| Metrics | CPU + Memory only |
| Collection | Localhost only (Cursor machine) |
| Add server fields | Name + IP/hostname |
| Auth | Single `admin` + hashed password |
| Refresh | Manual only |
| Screens | Login + Dashboard |
| Scale / UI | Max ~3 servers; UI libraries left open |
| Out of scope | Multi-user roles, Windows, history, alerts, cloud deploy |

---

## 2. Problem

Checking live memory, CPU, network, and port usage today requires logging into each Linux host. L1–L3 and app teams need a central, read-only view for routine checks.

**Demo note:** v1 delivers **CPU + Memory** only on **localhost**. Network and port views are deferred.

---

## 3. Goals and non-goals

### 3.1 Goals

- User-friendly **read-only** UI for metrics.
- Sign-in as **`admin`** with a **hashed** password.
- Provision to **add** Linux servers (Name + IP/hostname).
- Show **CPU %** and **memory** (used / free / total) for listed servers.
- **Manual refresh** only (button or page reload).
- Run locally with minimal steps.

### 3.2 Non-goals

- Multi-user admin / RBAC beyond the single demo login
- Windows hosts
- Long-term historical retention
- Email / ticket alerting
- Cloud or production deploy
- Network I/O, ports, disk, process list, uptime (not in option A)
- Auto-refresh / WebSockets
- Real remote SSH or agent collection (localhost demo only)

---

## 4. Users

| User | Need |
| --- | --- |
| L1 / L2 / L3 | Fast read-only CPU/memory check without SSH |
| App / infra engineers | Same demo UI for local walkthroughs |

All users share the single `admin` account in this demo.

---

## 5. Features

### 5.1 Read-only UI

- After login, show a simple dashboard of monitored servers with CPU and memory.
- Metrics views are **read-only**.
- Inventory add is allowed for the demo admin (up to ~3 servers).

### 5.2 Sign-in

- Default username: `admin`
- Password stored **hashed** (e.g. Werkzeug)
- Demo credentials documented in README only (local demo)

### 5.3 Add servers (Linux)

- Required fields: **Name**, **IP/hostname**
- Demo behavior: collection targets **localhost** (entries are inventory for the demo)
- Cap: **~3** servers

### 5.4 Metrics

- **CPU %**
- **Memory** (used / free / total)
- Updated only when the user manually refreshes

---

## 6. Screens (minimal)

1. **Login**
2. **Dashboard** — server list, CPU + memory, Add server (name + IP/hostname), Refresh

No Alerts, Settings, or Server detail pages in this baseline.

---

## 7. Technical notes (demo)

- **Backend:** Flask
- **Frontend:** Flask-rendered templates + attractive CSS
- **Storage:** local SQLite (or equivalent) for users/servers
- **Metrics source:** localhost / mock acceptable for demo
- **UI libs:** left open (custom CSS is fine)

---

## 8. Local run (minimal)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open `http://127.0.0.1:5000` and sign in as `admin` (password in README).

---

## 9. Acceptance criteria

- [ ] Unauthenticated users cannot see the dashboard
- [ ] `admin` logs in with hashed-password verification
- [ ] Dashboard is read-only for metrics and shows CPU % and memory
- [ ] Admin can add a server with **Name** and **IP/hostname** (up to ~3)
- [ ] Metrics update only on manual refresh
- [ ] App runs locally with the steps above

---

## 10. Decisions log

| Decision | Selection |
| --- | --- |
| Metrics | A — CPU + Memory only |
| Monitoring | A — localhost only |
| Add-server fields | A — Name + IP/hostname |
| Auth | A — single `admin` + hashed password |
| Refresh | A — manual only |
| Screens | A — Login + Dashboard |
| Scale / UI | A — ≤3 servers; UI libs open |
| Out of scope | A — no multi-user roles, Windows, history, alerts, cloud deploy |
