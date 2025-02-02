import pytest
from apps.admin_app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)
