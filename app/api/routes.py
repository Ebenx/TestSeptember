from fastapi import APIRouter, Depends, HTTPException

from app.schemas.ask import AskRequest, AskResponse
from app.schemas.process import ProcessRequest, ProcessResponse
from app.services.ollama_service import OllamaError, OllamaService, get_ollama_service
from app.services.process_service import ProcessService, get_process_service

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/process", response_model=ProcessResponse)
def process(
    request: ProcessRequest,
    service: ProcessService = Depends(get_process_service),
) -> ProcessResponse:
    return ProcessResponse(result=service.process(request.text))


@router.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
    service: OllamaService = Depends(get_ollama_service),
) -> AskResponse:
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        answer = service.ask(question)
    except OllamaError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return AskResponse(question=question, answer=answer)
