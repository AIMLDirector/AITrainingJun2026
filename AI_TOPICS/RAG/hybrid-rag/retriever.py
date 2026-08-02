from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchResults

from config import get_settings

settings = get_settings()

def get_dense_retriever() -> BaseRetriever:
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
    vectorstore = Chroma(
        persist_directory=settings.chroma_persist_dir,
        collection_name=settings.collection_name,
        embedding_function=embeddings,
    )
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.top_k},
    )

def get_sparse_retriever(documents: List[Document]) -> BM25Retriever:
    retriever = BM25Retriever.from_documents(documents)
    retriever.k = settings.top_k
    return retriever

def build_hybrid_retriever(documents: List[Document]) -> EnsembleRetriever:
    dense = get_dense_retriever()
    sparse = get_sparse_retriever(documents)
    return EnsembleRetriever(
        retrievers=[dense, sparse],
        weights=[settings.dense_weight, settings.sparse_weight],
    )

def get_web_search_tool():
    """Prefer Tavily (better quality). Falls back to DuckDuckGo if no key."""
    if settings.tavily_api_key:
        return TavilySearchResults(
            max_results=settings.web_search_results,
            api_key=settings.tavily_api_key,
            include_answer=False,
            include_raw_content=False,
        )
    else:
        return DuckDuckGoSearchResults(max_results=settings.web_search_results)