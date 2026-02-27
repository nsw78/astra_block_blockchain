"""Tests for admin API-key management endpoints."""


def test_create_key_requires_admin(client):
    resp = client.post("/api/v1/admin/keys", json={"name": "test"})
    assert resp.status_code == 403


def test_create_and_list_keys(client, admin_headers):
    resp = client.post("/api/v1/admin/keys", json={"name": "ci-test"}, headers=admin_headers)
    assert resp.status_code == 201
    key = resp.json()["key"]
    assert len(key) > 10

    resp = client.get("/api/v1/admin/keys", headers=admin_headers)
    assert resp.status_code == 200
    keys = resp.json()["keys"]
    assert any(k["key"] == key for k in keys)


def test_delete_key(client, admin_headers):
    resp = client.post("/api/v1/admin/keys", json={"name": "to-delete"}, headers=admin_headers)
    key = resp.json()["key"]

    resp = client.delete(f"/api/v1/admin/keys/{key}", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["deleted"] is True


def test_user_key_auth_flow(client, admin_headers):
    """Full lifecycle: create key via admin, use key for user endpoint."""
    resp = client.post("/api/v1/admin/keys", json={"name": "user-key"}, headers=admin_headers)
    user_key = resp.json()["key"]

    resp = client.get("/api/v1/documents/", headers={"X-API-Key": user_key})
    assert resp.status_code == 200
