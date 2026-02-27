"""
Shared test fixtures.
"""
import os
import pytest
from fastapi.testclient import TestClient

# ensure dev environment for tests
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("APIKEY_DB_PATH", "./data/test_apikeys.db")


@pytest.fixture(scope="session")
def client():
    """Provide a FastAPI TestClient that lives for the entire test session."""
    from app.main import create_app
    app = create_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def admin_headers():
    return {"X-API-Key": os.environ["ADMIN_API_KEY"]}
