from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status

from app.config import Settings, get_settings
from app.services.rag import RAGService


def get_rag_service(request: Request) -> RAGService:
    service: RAGService | None = getattr(request.app.state, "rag_service", None)
    if service is None or not service.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG service is not ready. Run POST /ingest first.",
        )
    return service


def verify_api_key(
    settings: Annotated[Settings, Depends(get_settings)],
    authorization: Annotated[str | None, Header()] = None,
) -> None:
    """Optional bearer-token guard for mutating endpoints."""
    if not settings.api_key:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.removeprefix("Bearer ").strip()
    if token != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
