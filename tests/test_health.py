from fastapi.testclient import TestClient

from backend.app.main import app


def test_root_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json()["project"] == "Capital OS"


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
