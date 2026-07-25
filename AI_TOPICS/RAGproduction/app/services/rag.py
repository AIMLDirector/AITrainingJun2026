import logging
from dataclasses import dataclass

from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from app.config import Settings
from app.schemas import QueryResponse, SourceDocument
from app.services import document_loader, vectorstore as vs

logger = logging.getLogger(__name__)


@dataclass
class RAGService:
    settings: Settings
    qa_chain: RetrievalQA | None = None
    vectorstore: object | None = None

    def initialize(self) -> None:
        if self.vectorstore is None:
            self.vectorstore = vs.get_vectorstore(self.settings)
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.settings.retriever_k}
        )
        llm = ChatOpenAI(
            model=self.settings.llm_model,
            temperature=self.settings.temperature,
            api_key=self.settings.openai_api_key,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        logger.info(
            "RAG ready — collection=%s docs=%s",
            self.settings.chroma_collection,
            vs.collection_count(self.vectorstore),
        )

    def is_ready(self) -> bool:
        return self.qa_chain is not None and self.vectorstore is not None

    def document_count(self) -> int | None:
        if self.vectorstore is None:
            return None
        return vs.collection_count(self.vectorstore)

    def query(self, question: str, top_k: int | None = None) -> QueryResponse:
        if not self.is_ready():
            raise RuntimeError("RAG service is not initialized")

        if top_k is not None:
            self.qa_chain.retriever.search_kwargs["k"] = top_k

        result = self.qa_chain.invoke({"query": question})
        answer = result.get("result", "")
        sources = [
            SourceDocument(
                content=doc.page_content,
                metadata=dict(doc.metadata or {}),
            )
            for doc in result.get("source_documents", [])
        ]
        return QueryResponse(answer=answer, sources=sources)

    def ingest(self) -> dict:
        docs = document_loader.load_documents(self.settings.data_dir, self.settings)
        if not docs:
            raise ValueError(
                f"No supported documents found in {self.settings.data_dir}"
            )

        chunks = document_loader.split_documents(docs, self.settings)

        # Release open DB handles before rebuilding on disk
        existing = self.vectorstore
        self.qa_chain = None
        self.vectorstore = None

        self.vectorstore = vs.rebuild_vectorstore(
            chunks, self.settings, existing=existing
        )
        self.initialize()
        return {
            "documents_loaded": len(docs),
            "chunks_created": len(chunks),
            "collection": self.settings.chroma_collection,
            "persist_directory": self.settings.chroma_dir,
        }
