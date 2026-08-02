from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from openai import APIError, AuthenticationError, RateLimitError

from AI_TOPICS.RAG.RAGproduction.app.api.deps import verify_api_key
from AI_TOPICS.RAG.RAGproduction.app.config import Settings, get_settings
from AI_TOPICS.RAG.RAGproduction.app.schemas import IngestResponse
from AI_TOPICS.RAG.RAGproduction.app.services.rag import RAGService

router = APIRouter(prefix="/v1", tags=["ingest"])


@router.post(
    "/ingest",
    response_model=IngestResponse,
    dependencies=[Depends(verify_api_key)],
)
def ingest(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> IngestResponse:
    service: RAGService | None = getattr(request.app.state, "rag_service", None)
    if service is None:
        service = RAGService(settings=settings)
        request.app.state.rag_service = service

    try:
        result = service.ingest()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OpenAI authentication failed. Check OPENAI_API_KEY.",
        ) from exc
    except RateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OpenAI rate limit or quota exceeded.",
        ) from exc
    except APIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI API error: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingest failed: {exc}",
        ) from exc

    return IngestResponse(**result)
