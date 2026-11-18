from app import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from app.models import User


def test_password_hashing_and_verify(app):
    with app.app_context():
        user = User.query.filter_by(username=DEFAULT_ADMIN_USERNAME).one()
        assert user.password_hash != DEFAULT_ADMIN_PASSWORD
        assert user.check_password(DEFAULT_ADMIN_PASSWORD) is True
        assert user.check_password("wrong-password") is False


def test_successful_login(client):
    response = client.post(
        "/login",
        data={
            "username": DEFAULT_ADMIN_USERNAME,
            "password": DEFAULT_ADMIN_PASSWORD,
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    home = client.get("/")
    assert home.status_code == 200
    assert DEFAULT_ADMIN_USERNAME.encode() in home.data


def test_failed_login(client):
    response = client.post(
        "/login",
        data={"username": DEFAULT_ADMIN_USERNAME, "password": "nope"},
        follow_redirects=True,
    )
    assert response.status_code == 401
    assert b"Invalid username or password." in response.data

    protected = client.get("/", follow_redirects=False)
    assert protected.status_code == 302
    assert "/login" in protected.headers["Location"]


def test_logout(client):
    client.post(
        "/login",
        data={
            "username": DEFAULT_ADMIN_USERNAME,
            "password": DEFAULT_ADMIN_PASSWORD,
        },
    )
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    protected = client.get("/", follow_redirects=False)
    assert protected.status_code == 302
    assert "/login" in protected.headers["Location"]


def test_protected_route_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_session_cookie_httponly(app, client):
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SECRET_KEY"]

    response = client.post(
        "/login",
        data={
            "username": DEFAULT_ADMIN_USERNAME,
            "password": DEFAULT_ADMIN_PASSWORD,
        },
    )
    set_cookies = response.headers.getlist("Set-Cookie")
    assert set_cookies
    assert any("HttpOnly" in value for value in set_cookies)
