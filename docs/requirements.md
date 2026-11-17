# Product Requirements Document (PRD)
## Demo Monitoring Infrastructure Application

| Field | Value |
| --- | --- |
| **Product** | Demo Monitoring Infrastructure |
| **Version** | 1.0 (Demo) |
| **Status** | Draft |
| **Audience** | Internal L1 / L2 / L3 infrastructure and application teams |
| **Deployment** | Local only (machine where Cursor is running) |
| **Document owner** | Engineering |

---

## 1. Summary

Build a **simple, local demo** web application that lets internal support and development teams view **read-only** Linux server metrics (CPU, memory, network, and port usage) without logging into each host.

For this demo:

- Metrics are **mocked** (no real SSH/agent collection).
- Server inventory and auth data persist in **SQLite**.
- UI is **Flask + Jinja templates + CSS** only.
- The dashboard **auto-refreshes every 5 seconds**.

---

## 2. Problem statement

Today, checking real-time memory, CPU, network, and port usage requires logging into individual Linux servers. That is slow for L1–L3 teams and makes routine health checks harder during incidents or handovers.

This demo shows a central, read-only UI for browsing monitored Linux servers and their current metrics from one place.

---

## 3. Goals and non-goals

### 3.1 Goals

- Provide a user-friendly, **read-only** monitoring UI.
- Support **sign-in** with a default `admin` account and a **hashed** password.
- Allow operators to **add Linux servers** to a monitored inventory (stored in SQLite).
- Display mock **CPU, memory, network, and port** metrics per server.
- Auto-refresh metrics every **5 seconds**.
- Run locally with a minimal Python/Flask setup.

### 3.2 Non-goals (out of scope for this demo)

- Alerts and notifications
- Multi-user accounts or role-based access (L1/L2/L3 distinctions are audience only; app has a single admin login)
- Windows host monitoring
- Long-term historical storage or trend analytics
- Mobile application
- Real metric collection (SSH, agents, SNMP, Prometheus, etc.)
- Password reset / SSO / MFA
- High availability, multi-instance deployment, or production hardening beyond basic demo needs

---

## 4. Users and use cases

### 4.1 Users

| Persona | Need |
| --- | --- |
| L1 support | Quickly check whether a named Linux server looks healthy |
| L2 infrastructure | Review CPU/memory/network/ports without host login |
| L3 / application teams | Confirm host/port visibility while troubleshooting |

All users share the same **admin** login for the demo. There are no distinct in-app roles.

### 4.2 Primary use cases

1. **Sign in** with `admin` and password.
2. **Add a Linux server** (name + host/IP + optional notes).
3. **View server list** and open a server detail view.
4. **Watch mock live metrics** refresh every 5 seconds.
5. **Sign out**.

---

## 5. Functional requirements

### 5.1 Authentication

| ID | Requirement |
| --- | --- |
| AUTH-01 | The app must require authentication for all monitoring pages. |
| AUTH-02 | Default username is `admin`. |
| AUTH-03 | The admin password must be stored **hashed** (e.g. Werkzeug/Passlib); never plain text in the database. |
| AUTH-04 | On first run (or seed), create the default admin user if it does not exist. |
| AUTH-05 | Failed login shows a generic error (do not reveal whether username or password was wrong). |
| AUTH-06 | Session-based login is sufficient (Flask session cookie). |
| AUTH-07 | Users can sign out and end the session. |

**Demo default credentials (document in README at implementation time):**

- Username: `admin`
- Password: a simple demo password (e.g. `admin123`) stored only as a hash after seed

### 5.2 Server inventory

| ID | Requirement |
| --- | --- |
| INV-01 | Authenticated users can add a Linux server to monitor. |
| INV-02 | Required fields: **display name**, **hostname or IP**. |
| INV-03 | Optional field: **notes** / description. |
| INV-04 | Server records persist in **SQLite**. |
| INV-05 | Authenticated users can view the list of monitored servers. |
| INV-06 | Authenticated users can open a detail page for one server. |
| INV-07 | Authenticated users can delete a server from inventory (keep UX simple; confirm before delete). |
| INV-08 | Duplicate hostname/IP may be allowed for demo simplicity, or blocked with a clear message—implementation should pick one and document it. **Preferred for demo:** block exact duplicate hostname/IP. |

> Inventory management (add/delete) is an operational exception to “read-only metrics.” Metric views themselves remain read-only.

### 5.3 Metrics (mock)

| ID | Requirement |
| --- | --- |
| MET-01 | For each server, show **CPU usage** (percent). |
| MET-02 | For each server, show **memory usage** (used / total and percent). |
| MET-03 | For each server, show **network usage** (e.g. mock RX/TX rates). |
| MET-04 | For each server, show **port usage** (list of mock listening ports with process/service name). |
| MET-05 | Metrics are **generated/mocked** in the application; no remote collection. |
| MET-06 | Mock values should look plausible and change slightly over time so auto-refresh feels “live.” |
| MET-07 | Metrics views are **read-only** (no edit/control actions on CPU, memory, network, or ports). |

### 5.4 Auto-refresh

| ID | Requirement |
| --- | --- |
| REF-01 | Server detail (and optionally the dashboard summary) auto-refreshes every **5 seconds**. |
| REF-02 | Refresh may use a simple page meta-refresh, lightweight JS `fetch` + DOM update, or full partial reload—prefer the simplest approach that keeps Jinja/CSS-first UX. |
| REF-03 | If refresh fails, show a non-blocking error state without crashing the page. |

### 5.5 UI / UX

| ID | Requirement |
| --- | --- |
| UI-01 | UI must be clear and usable for support engineers with minimal training. |
| UI-02 | Tech stack UI layer: **Flask + Jinja2 templates + CSS** only (no separate SPA framework). |
| UI-03 | Pages at minimum: Sign-in, Server list / dashboard, Add server, Server detail (metrics), Sign-out. |
| UI-04 | Visual design should look polished for a demo (clean layout, readable typography, clear status indicators) while staying CSS-only. |
| UI-05 | Metric pages are read-only; avoid controls that imply remote remediation. |

---

## 6. Data model (minimal)

### 6.1 `users`

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PK | |
| username | TEXT UNIQUE | Default seed: `admin` |
| password_hash | TEXT | Hashed password |
| created_at | TEXT/DATETIME | |

### 6.2 `servers`

| Column | Type | Notes |
| --- | --- | --- |
| id | INTEGER PK | |
| name | TEXT | Display name |
| host | TEXT | Hostname or IP |
| notes | TEXT NULL | Optional |
| created_at | TEXT/DATETIME | |

Mock metrics are **not** stored long-term. They are computed on request (and optionally cached briefly in memory). No historical metrics tables for this demo.

---

## 7. Technical requirements

| ID | Requirement |
| --- | --- |
| TECH-01 | Language: **Python 3**. |
| TECH-02 | Framework: **Flask**. |
| TECH-03 | Templates: **Jinja2**; styling: **CSS** (static files). |
| TECH-04 | Database: **SQLite** (local file, e.g. `instance/monitoring.db`). |
| TECH-05 | Run locally with a simple command (e.g. `flask run` or `python app.py`). |
| TECH-06 | Dependencies listed in `requirements.txt`. |
| TECH-07 | Configuration via environment variables or a small config module (secret key, DB path, refresh interval default `5`). |
| TECH-08 | Keep project structure small and easy to understand for demo purposes. |

### Suggested minimal layout

```text
Monitoring_Application/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── auth.py
│   ├── metrics.py          # mock metric generator
│   ├── templates/
│   └── static/css/
├── instance/               # SQLite DB (gitignored)
├── docs/
│   └── requirements.md
├── requirements.txt
└── README.md
```

---

## 8. Security requirements (demo-appropriate)

| ID | Requirement |
| --- | --- |
| SEC-01 | Store passwords hashed only. |
| SEC-02 | Protect routes behind login. |
| SEC-03 | Use a Flask `SECRET_KEY` for sessions. |
| SEC-04 | Basic CSRF protection on form posts is desirable if easy with chosen Flask extensions; otherwise document as a known demo limitation. |
| SEC-05 | Do not expose the SQLite file via static routes. |
| SEC-06 | This is a **local demo**—not production-ready security. |

---

## 9. Acceptance criteria

The demo is acceptable when all of the following are true:

1. App starts locally with documented steps.
2. User can sign in as `admin` with the seeded password.
3. Password in SQLite is hashed, not plain text.
4. User can add a Linux server (name + host) and see it in the list.
5. User can open a server and see mock CPU, memory, network, and port metrics.
6. Metrics update automatically about every 5 seconds.
7. Metric screens are read-only.
8. Server inventory persists across app restarts (SQLite).
9. User can sign out and cannot access monitoring pages until signing in again.
10. No features from the non-goals list are required for demo completion.

---

## 10. Setup assumptions (minimal)

- Single developer machine / local Cursor environment.
- No Docker required for v1 unless added later for convenience.
- No external monitoring backends.
- Browser access via `http://127.0.0.1:<port>`.

---

## 11. Future enhancements (not in this demo)

- Real collection via SSH or host agents
- Historical charts and retention policy
- Alerts / thresholds / notifications
- Multi-user roles (L1/L2/L3 permissions)
- Windows and other OS support
- Hardened production deployment

---

## 12. Open decisions (resolved for this PRD)

| Topic | Decision |
| --- | --- |
| Metrics source | Mock data |
| Persistence | SQLite |
| Refresh | Auto-refresh every 5 seconds |
| UI stack | Flask + Jinja + CSS only |
| Scope exclusions | Alerts, notifications, multi-user roles, Windows hosts, long-term history, mobile app |
| Deployment | Local demo only |
