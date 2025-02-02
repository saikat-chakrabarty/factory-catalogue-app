import pytest
from fastapi.testclient import TestClient
from apps.admin_app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_health():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] in ["ok", "fail"]
