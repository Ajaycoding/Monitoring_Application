from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.auth import login_required
from app.models import User

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def home():
    """Protected placeholder home / dashboard page."""
    return render_template("home.html", username=session.get("username"))


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
