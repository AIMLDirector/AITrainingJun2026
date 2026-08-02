import streamlit as st
from pathlib import Path
import time
import re

from config import get_settings
from ingest import load_documents, split_documents, build_vectorstore
from chain import create_full_rag_chain

st.set_page_config(
    page_title="Hybrid RAG + Web Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

settings = get_settings()

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔍 Hybrid RAG + Web")
    st.caption("Internal (Dense + BM25) + External Web Search")
    st.divider()

    st.subheader("Retrieval Settings")
    top_k = st.slider("Top-K (Internal)", 3, 12, settings.top_k)
    dense_w = st.slider("Dense weight", 0.0, 1.0, settings.dense_weight, 0.05)
    st.write(f"Sparse weight: `{1 - dense_w:.2f}`")

    st.divider()
    st.subheader("Documents")
    uploaded = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

    if uploaded:
        data_dir = Path("./data")
        data_dir.mkdir(exist_ok=True)
        for f in uploaded:
            (data_dir / f.name).write_bytes(f.read())
        st.success(f"Saved {len(uploaded)} file(s)")

    if st.button("🔄 Rebuild Index", type="primary", use_container_width=True):
        with st.spinner("Ingesting documents..."):
            docs = load_documents("./data")
            chunks = split_documents(docs)
            if chunks:
                build_vectorstore(chunks)
                st.session_state.chunks = chunks
                st.session_state.chain = create_full_rag_chain(chunks)
                st.success(f"Indexed {len(chunks)} chunks")
            else:
                st.warning("No PDFs found in ./data")

    st.divider()
    st.caption(f"Web Search: {'Tavily' if settings.tavily_api_key else 'DuckDuckGo (free)'}")

# ---------- Main ----------
st.title("Hybrid RAG + Web Search")
st.caption("Internal knowledge base + Live web search → Structured answer")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    st.session_state.chain = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []

# Auto-load
if st.session_state.chain is None:
    with st.spinner("Loading existing index..."):
        docs = load_documents("./data")
        chunks = split_documents(docs)
        if chunks:
            st.session_state.chunks = chunks
            st.session_state.chain = create_full_rag_chain(chunks)

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything (searches both internal docs + web)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.chain is None:
            st.error("No documents indexed yet. Upload PDFs and click **Rebuild Index**.")
        else:
            with st.spinner("Searching internal docs + web..."):
                start = time.time()
                try:
                    full_response = st.session_state.chain.invoke(prompt)
                    latency = time.time() - start

                    # Display the structured response
                    st.markdown(full_response)
                    st.caption(f"⏱️ {latency:.2f}s · Hybrid Internal + Web Search")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.caption(
    f"Model: `{settings.chat_model}` · "
    f"Chunks loaded: {len(st.session_state.chunks)} · "
    f"Web: {'Tavily' if settings.tavily_api_key else 'DuckDuckGo'}"
)