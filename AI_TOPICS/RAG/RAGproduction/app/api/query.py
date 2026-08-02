from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from openai import APIError, AuthenticationError, RateLimitError

from AI_TOPICS.RAG.RAGproduction.app.api.deps import get_rag_service
from AI_TOPICS.RAG.RAGproduction.app.schemas import QueryRequest, QueryResponse
from AI_TOPICS.RAG.RAGproduction.app.services.rag import RAGService

router = APIRouter(prefix="/v1", tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query(
    body: QueryRequest,
    rag: Annotated[RAGService, Depends(get_rag_service)],
) -> QueryResponse:
    try:
        return rag.query(body.question, top_k=body.top_k)
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
            detail=f"Query failed: {exc}",
        ) from exc
