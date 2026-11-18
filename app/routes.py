from __future__ import annotations

import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.auth import login_required
from app.metrics import collect_localhost_metrics
from app.models import MAX_SERVERS, Server, User, db

bp = Blueprint("main", __name__)

# Allow simple hostnames / IPv4-looking strings; reject shell metacharacters.
_HOST_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,253}$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._/-]{0,78}$")


def _validate_server_fields(name: str, ip_hostname: str) -> str | None:
    """Return an error message, or None if valid."""
    if not name:
        return "Name is required."
    if not ip_hostname:
        return "IP / hostname is required."
    if not _NAME_RE.match(name):
        return "Name contains invalid characters."
    if not _HOST_RE.match(ip_hostname):
        return "IP / hostname contains invalid characters."
    return None


@bp.route("/")
@login_required
def home():
    """Protected dashboard: inventory + read-only localhost metrics."""
    servers = Server.query.order_by(Server.created_at.asc()).all()
    # One localhost snapshot shared by all rows (demo collection model).
    metrics = collect_localhost_metrics()
    return render_template(
        "home.html",
        username=session.get("username"),
        servers=servers,
        metrics=metrics,
        server_count=len(servers),
        max_servers=MAX_SERVERS,
        can_add=len(servers) < MAX_SERVERS,
    )


@bp.route("/servers", methods=["POST"])
@login_required
def add_server():
    """Add a Linux server inventory entry (Name + IP/hostname)."""
    name = (request.form.get("name") or "").strip()
    ip_hostname = (request.form.get("ip_hostname") or "").strip()

    error = _validate_server_fields(name, ip_hostname)
    if error:
        flash(error, "error")
        return redirect(url_for("main.home"))

    if Server.query.count() >= MAX_SERVERS:
        flash(f"Demo limit reached: at most {MAX_SERVERS} servers.", "error")
        return redirect(url_for("main.home"))

    db.session.add(Server(name=name, ip_hostname=ip_hostname))
    db.session.commit()
    flash(f"Added server “{name}”.", "ok")
    return redirect(url_for("main.home"))


@bp.route("/refresh")
@login_required
def refresh():
    """Manual refresh — reloads dashboard metrics (no auto-refresh)."""
    return redirect(url_for("main.home"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.home"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            # Generic message — do not reveal which field was wrong.
            flash("Invalid username or password.", "error")
            return render_template("login.html"), 401

        session.clear()
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("main.home"))

    return render_template("login.html")


@bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect(url_for("main.login"))
