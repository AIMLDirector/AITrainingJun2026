import gc
import logging
import shutil
import time
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from AI_TOPICS.RAG.RAGproduction.app.config import Settings

logger = logging.getLogger(__name__)


def build_embeddings(settings: Settings) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )


def get_vectorstore(settings: Settings, embeddings: OpenAIEmbeddings | None = None) -> Chroma:
    embeddings = embeddings or build_embeddings(settings)
    Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=settings.chroma_collection,
        persist_directory=settings.chroma_dir,
        embedding_function=embeddings,
    )


def collection_count(vectorstore: Chroma) -> int:
    try:
        return int(vectorstore._collection.count())
    except Exception:
        logger.exception("Unable to read collection count")
        return 0


def _detach_vectorstore(vectorstore: Chroma | None) -> None:
    """Drop open Chroma client refs without mutating the on-disk schema."""
    if vectorstore is None:
        return
    for attr in ("_client", "_collection", "_embedding_function"):
        if hasattr(vectorstore, attr):
            try:
                object.__setattr__(vectorstore, attr, None)
            except Exception:
                try:
                    setattr(vectorstore, attr, None)
                except Exception:
                    pass
    gc.collect()
    time.sleep(0.25)


def rebuild_vectorstore(
    chunks: list[Document],
    settings: Settings,
    existing: Chroma | None = None,
) -> Chroma:
    """Replace the persisted store with freshly embedded chunks."""
    _detach_vectorstore(existing)

    chroma_path = Path(settings.chroma_dir).resolve()
    if chroma_path.exists():
        shutil.rmtree(chroma_path, ignore_errors=True)
        # Brief pause so SQLite / OS release file locks (esp. on macOS)
        time.sleep(0.35)
    chroma_path.mkdir(parents=True, exist_ok=True)

    embeddings = build_embeddings(settings)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_path),
        collection_name=settings.chroma_collection,
    )
    logger.info(
        "Rebuilt collection '%s' with %d chunks at %s",
        settings.chroma_collection,
        collection_count(vectorstore),
        chroma_path,
    )
    return vectorstore
