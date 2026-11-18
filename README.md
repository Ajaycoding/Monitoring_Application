# Demo Monitoring Infrastructure

Local demo web app for browsing **read-only Linux CPU % and memory** from a simple Flask + Jinja + CSS UI.

This is a **local demo only** — not production-ready. Metrics are collected from **localhost** only; inventory IP/hostname fields are display-only (no SSH/agent).

## Requirements

- **Python 3.10+** (Linux recommended for `/proc` metrics)

## Quick start

```bash
# From the project root
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=app:create_app
export FLASK_DEBUG=1               # optional, local reloads
# Optional: override the session secret (recommended even for local use)
# export SECRET_KEY="your-local-secret"

flask run
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Demo credentials (demo only)

| Field | Value |
| --- | --- |
| Username | `admin` |
| Password | `admin123` |

On first run the app seeds this user into SQLite with a **hashed** password (never stored plain text). Auth is session-based; the dashboard requires sign-in. Unauthenticated requests redirect to `/login`. Sign out via **Sign out**.

**Warning:** These credentials are for the local demo only. Do not reuse them elsewhere.

## UI tour (minimal)

1. Sign in as `admin`
2. **Add server** with **Name** + **IP/hostname** (max **3**)
3. View **CPU %** and **memory** (used / free / total) on the dashboard
4. Click **Refresh metrics** to update values (manual only — no auto-refresh)

## Inventory & metrics notes

| Topic | Behavior |
| --- | --- |
| Add fields | `Name`, `IP / hostname` |
| Cap | At most 3 servers |
| Persistence | SQLite under `instance/` (gitignored) |
| Metrics source | This machine via `/proc` (localhost) |
| Remote hosts | Not contacted; IP/hostname is label-only |
| Refresh | Manual button / page load only |
| CSRF | Not enabled — local demo limitation |

## Tests

```bash
source .venv/bin/activate
pytest
```

## CI

GitHub Actions runs a minimal workflow (`.github/workflows/ci.yml`) on pushes and pull requests to `main` or `master`:

1. Check out the repo
2. Set up **Python 3.10**
3. Install dependencies from `requirements.txt`
4. Run `pytest`

There is no deploy step and no production secrets — CI uses a throwaway `SECRET_KEY` for tests only.

## Configuration

| Variable | Purpose | Local default |
| --- | --- | --- |
| `FLASK_APP` | App entrypoint | `app:create_app` (set when running) |
| `SECRET_KEY` | Flask session signing | `dev-only-change-me-local-demo` if unset |
| `DATABASE_URL` | SQLAlchemy DB URI | `sqlite:///…/instance/monitoring.db` |

**Security:** Do not commit real secrets. Prefer setting `SECRET_KEY` via the environment. Session cookies are `HttpOnly`. Passwords are hashed. Metrics code never shells out or calls inventory hosts.

## Project layout

```text
Monitoring_Application/
├── app/
│   ├── __init__.py          # create_app factory + admin seed
│   ├── auth.py              # login_required
│   ├── metrics.py           # localhost CPU + memory
│   ├── models.py            # User, Server + db
│   ├── routes.py
│   ├── templates/
│   └── static/css/
├── instance/                # SQLite DB (gitignored)
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## Status

Steps 1–9 from [`docs/TODO.md`](docs/TODO.md) are implemented against [`docs/requirements.md`](docs/requirements.md).
