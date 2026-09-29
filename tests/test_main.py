from fastapi.testclient import TestClient

from app.main import app
from app.services.process_service import ProcessService, get_process_service

client = TestClient(app)


def test_process_echoes_text():
    response = client.post("/process", json={"text": "hola"})
    assert response.status_code == 200
    assert response.json() == {"result": "hola"}


def test_process_rejects_missing_text():
    response = client.post("/process", json={})
    assert response.status_code == 422


def test_process_uses_injected_service():
    class FakeService(ProcessService):
        def process(self, text: str) -> str:
            return "fake"

    app.dependency_overrides[get_process_service] = lambda: FakeService()
    try:
        response = client.post("/process", json={"text": "hola"})
        assert response.json() == {"result": "fake"}
    finally:
        app.dependency_overrides.clear()
