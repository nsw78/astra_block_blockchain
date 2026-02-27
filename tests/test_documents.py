"""Tests for RAG / document endpoints."""


def test_search_documents(client):
    resp = client.get("/api/v1/documents/search", params={"q": "owner drain", "k": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "owner drain"
    assert isinstance(data["results"], list)


def test_index_docs_requires_auth(client):
    resp = client.post("/api/v1/documents/", json={"docs": ["test doc"]})
    assert resp.status_code == 401


def test_list_docs_requires_auth(client):
    resp = client.get("/api/v1/documents/")
    assert resp.status_code == 401


def test_index_and_list_docs(client, admin_headers):
    resp = client.post(
        "/api/v1/documents/",
        json={"docs": ["new test document"], "ids": ["test_1"]},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["indexed"] == 1

    resp = client.get("/api/v1/documents/", headers=admin_headers)
    assert resp.status_code == 200
    assert "test_1" in resp.json()["docs"]
