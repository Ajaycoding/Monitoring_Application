from app import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from app.models import MAX_SERVERS, Server


def _login(client):
    return client.post(
        "/login",
        data={
            "username": DEFAULT_ADMIN_USERNAME,
            "password": DEFAULT_ADMIN_PASSWORD,
        },
    )


def test_add_and_list_servers(client, app):
    _login(client)
    response = client.post(
        "/servers",
        data={"name": "local-demo", "ip_hostname": "127.0.0.1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"local-demo" in response.data
    assert b"127.0.0.1" in response.data

    with app.app_context():
        assert Server.query.count() == 1


def test_reject_empty_server_fields(client, app):
    _login(client)
    response = client.post(
        "/servers",
        data={"name": "", "ip_hostname": "127.0.0.1"},
        follow_redirects=True,
    )
    assert b"Name is required." in response.data
    with app.app_context():
        assert Server.query.count() == 0


def test_reject_invalid_hostname_characters(client, app):
    _login(client)
    response = client.post(
        "/servers",
        data={"name": "bad", "ip_hostname": "127.0.0.1;rm -rf /"},
        follow_redirects=True,
    )
    assert b"IP / hostname contains invalid characters." in response.data
    with app.app_context():
        assert Server.query.count() == 0


def test_reject_over_server_cap(client, app):
    _login(client)
    for i in range(MAX_SERVERS):
        client.post(
            "/servers",
            data={"name": f"srv-{i}", "ip_hostname": f"127.0.0.{i + 1}"},
        )
    response = client.post(
        "/servers",
        data={"name": "overflow", "ip_hostname": "10.0.0.9"},
        follow_redirects=True,
    )
    assert b"Demo limit reached" in response.data
    with app.app_context():
        assert Server.query.count() == MAX_SERVERS


def test_inventory_requires_auth(client):
    response = client.post(
        "/servers",
        data={"name": "x", "ip_hostname": "127.0.0.1"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
