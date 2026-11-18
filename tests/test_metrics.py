from app import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from app.metrics import collect_localhost_metrics, get_cpu_percent, get_memory_stats


def _login(client):
    client.post(
        "/login",
        data={
            "username": DEFAULT_ADMIN_USERNAME,
            "password": DEFAULT_ADMIN_PASSWORD,
        },
    )


def test_cpu_percent_shape_and_range():
    value = get_cpu_percent(sample_seconds=0.05)
    assert isinstance(value, float)
    assert 0.0 <= value <= 100.0


def test_memory_stats_fields():
    mem = get_memory_stats()
    for key in (
        "used_bytes",
        "free_bytes",
        "total_bytes",
        "used_human",
        "free_human",
        "total_human",
    ):
        assert key in mem
    assert mem["total_bytes"] > 0
    assert mem["used_bytes"] >= 0
    assert mem["free_bytes"] >= 0
    assert mem["used_bytes"] + mem["free_bytes"] <= mem["total_bytes"] + 1024


def test_collect_localhost_metrics_bundle():
    snapshot = collect_localhost_metrics(sample_seconds=0.05)
    assert snapshot["source"] == "localhost"
    assert 0.0 <= snapshot["cpu_percent"] <= 100.0
    assert "used_human" in snapshot["memory"]


def test_dashboard_shows_metrics_when_server_exists(client):
    _login(client)
    client.post(
        "/servers",
        data={"name": "metrics-box", "ip_hostname": "127.0.0.1"},
    )
    response = client.get("/")
    assert response.status_code == 200
    assert b"metrics-box" in response.data
    assert b"CPU" in response.data
    assert b"Memory" in response.data or b"memory" in response.data
    assert b"%" in response.data
    assert b"localhost" in response.data


def test_refresh_requires_auth(client):
    response = client.get("/refresh", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_refresh_redirects_authenticated(client):
    _login(client)
    response = client.get("/refresh", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
