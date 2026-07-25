import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, ingest, query
from app.config import get_settings
from app.services import document_loader
from app.services.rag import RAGService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    document_loader.ensure_data_dir(settings.data_dir)

    rag_service = RAGService(settings=settings)
    try:
        rag_service.initialize()
        count = rag_service.document_count() or 0
        if count == 0:
            logger.warning(
                "Vector store is empty. Call POST /v1/ingest after placing files in %s",
                settings.data_dir,
            )
    except Exception:
        logger.exception(
            "Failed to initialize RAG on startup; /health will report degraded until ingest succeeds"
        )

    app.state.rag_service = rag_service
    logger.info("%s v%s started", settings.app_name, settings.app_version)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    if settings.debug:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.include_router(health.router)
    app.include_router(query.router)
    app.include_router(ingest.router)
    return app


app = create_app()
