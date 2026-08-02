import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.documents import Document

from config import get_settings
from ingest import load_documents, split_documents
from chain import create_rag_chain

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hybrid-rag")

settings = get_settings()
rag_chain = None
all_chunks: list[Document] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_chain, all_chunks
    logger.info("Loading documents & building hybrid chain...")
    raw_docs = load_documents("./data")
    all_chunks = split_documents(raw_docs)
    if not all_chunks:
        logger.warning("No documents found. Add PDFs to ./data")
    else:
        rag_chain = create_rag_chain(all_chunks)
    logger.info("Ready")
    yield

app = FastAPI(title="Hybrid RAG API", version="1.0.0", lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)

class QueryResponse(BaseModel):
    answer: str
    question: str

@app.get("/health")
async def health():
    return {"status": "ok", "docs_loaded": len(all_chunks)}

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    if rag_chain is None:
        raise HTTPException(503, "Service not ready or no documents")
    try:
        answer = await rag_chain.ainvoke(req.question)
        return QueryResponse(answer=answer, question=req.question)
    except Exception as e:
        logger.exception("Query failed")
        raise HTTPException(500, str(e))