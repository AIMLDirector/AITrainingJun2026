from typing import Annotated

from fastapi import APIRouter, Depends, Request

from AI_TOPICS.RAG.RAGproduction.app.config import Settings, get_settings
from AI_TOPICS.RAG.RAGproduction.app.schemas import HealthResponse
from AI_TOPICS.RAG.RAGproduction.app.services.rag import RAGService
from AI_TOPICS.RAG.RAGproduction.app.services import vectorstore as vs

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    service: RAGService | None = getattr(request.app.state, "rag_service", None)
    ready = bool(service and service.is_ready())
    count = service.document_count() if ready else None
    if count is None and service and service.vectorstore is not None:
        count = vs.collection_count(service.vectorstore)

    return HealthResponse(
        status="ok" if ready else "degraded",
        app=settings.app_name,
        version=settings.app_version,
        vectorstore_ready=ready,
        document_count=count,
    )
