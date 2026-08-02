from typing import List, Dict, Any
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

from config import get_settings
from retriever import build_hybrid_retriever, get_web_search_tool

settings = get_settings()

# ---------- Formatters ----------
def format_internal_docs(docs: List[Document]) -> str:
    if not docs:
        return "No relevant internal documents found."
    return "\n\n---\n\n".join(
        f"**Source:** {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )

def format_web_results(results: List[Dict[str, Any]]) -> str:
    if not results:
        return "No relevant web results found."
    
    formatted = []
    for i, r in enumerate(results, 1):
        title = r.get("title") or r.get("link", "No title")
        url = r.get("link") or r.get("url", "")
        content = r.get("content") or r.get("snippet", "")
        formatted.append(f"**[{i}] {title}**\nURL: {url}\n{content}")
    return "\n\n".join(formatted)

# ---------- Main Chain ----------
STRUCTURED_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert research assistant.
You will receive two sources of information:
1. Internal documents (from the company's knowledge base)
2. External web search results

Your job is to produce a clear, well-structured response in **exactly** this markdown format:

### Internal Search Output
Summarize and present the most relevant information found in the internal documents.
If nothing relevant was found, say so clearly.

### External Search Output
Summarize the key findings from the web search results. Include important facts, recent information, and cite the sources by number when possible.

### Consolidated Answer
Give a final, well-reasoned answer that combines both internal and external knowledge.
Clearly indicate what comes from internal documents vs external sources.
If the sources conflict, point it out. Be accurate and concise.

Question: {question}
"""),
    ("human", """### Internal Documents
{internal_context}

### Web Search Results
{web_context}

Please answer following the exact structure above.""")
])

def create_full_rag_chain(documents: List[Document]):
    hybrid_retriever = build_hybrid_retriever(documents)
    web_tool = get_web_search_tool()
    llm = ChatOpenAI(
        model=settings.chat_model,
        temperature=0.15,
        api_key=settings.openai_api_key,
    )

    def run_web_search(query: str):
        try:
            return web_tool.invoke(query)
        except Exception as e:
            return [{"title": "Web search failed", "content": str(e), "link": ""}]

    chain = (
        RunnableParallel(
            question=RunnablePassthrough(),
            internal_docs=hybrid_retriever,
            web_results=RunnableLambda(run_web_search),
        )
        | RunnableParallel(
            question=itemgetter("question"),
            internal_context=itemgetter("internal_docs") | RunnableLambda(format_internal_docs),
            web_context=itemgetter("web_results") | RunnableLambda(format_web_results),
            # Keep raw for optional future use
            raw_internal=itemgetter("internal_docs"),
            raw_web=itemgetter("web_results"),
        )
        | STRUCTURED_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain