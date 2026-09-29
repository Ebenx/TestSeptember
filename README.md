# TestSeptember

Minimal FastAPI service with a POST endpoint.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

```bash
curl -X POST http://127.0.0.1:8000/process -H "Content-Type: application/json" -d '{"text": "hola"}'
```

## Test

```bash
pytest
```
