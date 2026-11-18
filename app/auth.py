from functools import wraps

from flask import redirect, session, url_for


def login_required(view):
    """Redirect unauthenticated users to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped
