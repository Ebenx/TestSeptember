from fastapi.testclient import TestClient

from app.main import app
from app.services.ollama_service import OllamaError, OllamaService, get_ollama_service

client = TestClient(app)


class FakeOllama(OllamaService):
    def __init__(self, answer: str | None = None, error: OllamaError | None = None):
        self.answer = answer
        self.error = error

    def ask(self, question: str) -> str:
        if self.error:
            raise self.error
        return self.answer


def _override(service: OllamaService):
    app.dependency_overrides[get_ollama_service] = lambda: service


def test_ask_returns_answer():
    _override(FakeOllama(answer="Paris"))
    try:
        response = client.post("/ask", json={"question": "Capital de Francia?"})
        assert response.status_code == 200
        assert response.json() == {"question": "Capital de Francia?", "answer": "Paris"}
    finally:
        app.dependency_overrides.clear()


def test_ask_rejects_empty_question():
    for body in ({"question": ""}, {"question": "   "}, {}):
        response = client.post("/ask", json=body)
        assert response.status_code == 400
        assert response.json() == {"detail": "La pregunta no puede estar vacía"}


def test_ask_propagates_ollama_error():
    _override(FakeOllama(error=OllamaError("caído", 503)))
    try:
        response = client.post("/ask", json={"question": "hola"})
        assert response.status_code == 503
        assert response.json() == {"detail": "caído"}
    finally:
        app.dependency_overrides.clear()
