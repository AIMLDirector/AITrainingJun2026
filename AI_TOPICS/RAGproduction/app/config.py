from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "RAG Production API"
    app_version: str = "1.0.0"
    debug: bool = False

    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.0

    chroma_dir: str = "../rag_chroma_db"
    chroma_collection: str = "books"
    data_dir: str = "../data"
    # Comma-separated; CSV is off by default (large files blow OpenAI rate limits)
    ingest_extensions: str = ".pdf,.txt"
    retriever_k: int = 4
    chunk_size: int = 1000
    chunk_overlap: int = 200

    host: str = "0.0.0.0"
    port: int = 8000
    api_key: str | None = None  # optional bearer token for write endpoints

    @property
    def allowed_extensions(self) -> set[str]:
        return {
            ext.strip().lower() if ext.strip().startswith(".") else f".{ext.strip().lower()}"
            for ext in self.ingest_extensions.split(",")
            if ext.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
