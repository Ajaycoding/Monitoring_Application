import os

from flask import Flask

from app.models import User, db

# Demo-only default password (stored hashed). Documented in README.
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


def seed_admin() -> None:
    """Create the default admin user on first run if missing."""
    if User.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first() is not None:
        return
    user = User(username=DEFAULT_ADMIN_USERNAME)
    user.set_password(DEFAULT_ADMIN_PASSWORD)
    db.session.add(user)
    db.session.commit()


def create_app(test_config=None):
    """Application factory for the demo monitoring app."""
    app = Flask(__name__, instance_relative_config=True)

    # Prefer SECRET_KEY from the environment; fall back to a local demo default.
    # Do not use the default outside local development.
    default_db = "sqlite:///" + os.path.join(app.instance_path, "monitoring.db")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me-local-demo"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", default_db),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
    )

    if test_config is not None:
        app.config.update(test_config)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be a non-empty value")

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)

    from app.routes import bp

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
        seed_admin()

    return app
