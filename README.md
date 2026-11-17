# Demo Monitoring Infrastructure

Local demo web app for browsing **mock** Linux server metrics (CPU, memory, network, ports) from a single Flask + Jinja + CSS UI.

This is a **local demo only** — not production-ready. Metrics are mocked; there is no real SSH/agent collection yet.

## Requirements

- **Python 3.10+** (3.x)

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

Equivalent:

```bash
python -m flask run
```

## Demo credentials (demo only)

| Field | Value |
| --- | --- |
| Username | `admin` |
| Password | `admin123` |

On first run the app seeds this user into SQLite with a **hashed** password (never stored plain text). Auth is session-based; the home page and other monitoring routes require sign-in. Unauthenticated requests are redirected to `/login`. Sign out via **Sign out** (or `/logout`).

**Warning:** These credentials are for the local demo only. Do not reuse them elsewhere.

## Tests

```bash
source .venv/bin/activate
pytest
```

## Configuration

| Variable | Purpose | Local default |
| --- | --- | --- |
| `FLASK_APP` | App entrypoint | `app:create_app` (set when running) |
| `SECRET_KEY` | Flask session signing | `dev-only-change-me-local-demo` if unset |
| `DATABASE_URL` | SQLAlchemy DB URI | `sqlite:///…/instance/monitoring.db` |

**Security:** Do not commit real secrets. Prefer setting `SECRET_KEY` via the environment. The built-in default is for local demo convenience only. Session cookies are `HttpOnly`.

## Project layout

```text
Monitoring_Application/
├── app/
│   ├── __init__.py          # create_app factory + admin seed
│   ├── auth.py              # login_required
│   ├── models.py            # User + db
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

Phases 0–1 are in place (scaffold + sign-in). Server inventory and mock metrics come next — see [`docs/TODO.md`](docs/TODO.md) and [`docs/requirements.md`](docs/requirements.md).
