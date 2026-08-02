from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str
    tavily_api_key: str | None = None          # optional but recommended

    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"
    chroma_persist_dir: str = "./chroma_db"
    collection_name: str = "hybrid_rag"
    chunk_size: int = 800
    chunk_overlap: int = 150
    top_k: int = 6
    dense_weight: float = 0.55
    sparse_weight: float = 0.45
    web_search_results: int = 5

@lru_cache()
def get_settings() -> Settings:
    return Settings()