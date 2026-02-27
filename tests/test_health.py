"""Tests for health & readiness endpoints."""


def test_health(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_readiness(client):
    resp = client.get("/api/v1/readiness")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "degraded")
    assert len(data["checks"]) >= 1


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "AstraBlock"


def test_request_id_header(client):
    resp = client.get("/api/v1/health")
    assert "x-request-id" in resp.headers


def test_security_headers(client):
    resp = client.get("/api/v1/health")
    assert resp.headers.get("x-content-type-options") == "nosniff"
    assert resp.headers.get("x-frame-options") == "DENY"
