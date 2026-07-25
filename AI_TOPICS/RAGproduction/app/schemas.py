from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    top_k: int | None = Field(default=None, ge=1, le=20)


class SourceDocument(BaseModel):
    content: str
    metadata: dict


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument] = []


class IngestResponse(BaseModel):
    documents_loaded: int
    chunks_created: int
    collection: str
    persist_directory: str


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    vectorstore_ready: bool
    document_count: int | None = None
