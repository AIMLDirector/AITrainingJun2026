import logging
import os
from pathlib import Path

from langchain_community.document_loaders import CSVLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from AI_TOPICS.RAG.RAGproduction.app.config import Settings

logger = logging.getLogger(__name__)

LOADER_BY_EXT = {
    ".pdf": lambda path: PyPDFLoader(str(path)),
    ".txt": lambda path: TextLoader(str(path), encoding="utf-8"),
    ".csv": lambda path: CSVLoader(str(path)),
}


def load_documents(data_dir: str, settings: Settings | None = None) -> list[Document]:
    """Load documents whose extensions are allowed by settings."""
    allowed = (
        settings.allowed_extensions
        if settings is not None
        else {".pdf", ".txt"}
    )
    root = Path(data_dir)
    if not root.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    docs: list[Document] = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()
        if suffix not in allowed:
            logger.info("Skipping %s (extension not in %s)", path.name, sorted(allowed))
            continue
        if suffix not in LOADER_BY_EXT:
            logger.info("Skipping unsupported file: %s", path.name)
            continue

        try:
            loader = LOADER_BY_EXT[suffix](path)
            loaded = loader.load()
            for doc in loaded:
                doc.metadata = {
                    "source": path.name,
                    **{k: v for k, v in doc.metadata.items() if k != "source"},
                }
            docs.extend(loaded)
            logger.info("Loaded %s (%d parts)", path.name, len(loaded))
        except Exception:
            logger.exception("Failed to load %s", path.name)
            raise

    return docs


def split_documents(docs: list[Document], settings: Settings) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(docs)


def ensure_data_dir(data_dir: str) -> None:
    os.makedirs(data_dir, exist_ok=True)
