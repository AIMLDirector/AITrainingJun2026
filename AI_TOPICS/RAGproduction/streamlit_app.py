"""Simple Streamlit UI that talks to the RAG FastAPI backend."""

import requests
import streamlit as st

st.set_page_config(page_title="RAG Chat", page_icon="📚", layout="centered")
st.title("RAG Chat")
st.caption("Ask questions against your FastAPI + Chroma knowledge base.")

# --- Sidebar: API connection ---
with st.sidebar:
    st.header("API settings")
    api_base = st.text_input(
        "FastAPI base URL",
        value="http://127.0.0.1:8000",
        help="Where uvicorn / docker is serving the API",
    ).rstrip("/")
    api_key = st.text_input(
        "API key (optional)",
        type="password",
        help="Bearer token if API_KEY is set on the server",
    )
    top_k = st.slider("Top-k sources", min_value=1, max_value=10, value=4)

    def _headers() -> dict:
        headers = {"Content-Type": "application/json"}
        if api_key.strip():
            headers["Authorization"] = f"Bearer {api_key.strip()}"
        return headers

    if st.button("Check health", use_container_width=True):
        try:
            resp = requests.get(f"{api_base}/health", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data.get("vectorstore_ready"):
                st.success(
                    f"OK — {data.get('document_count', 0)} docs in vector store"
                )
            else:
                st.warning("API up, but vector store not ready. Run ingest.")
            st.json(data)
        except requests.RequestException as exc:
            st.error(f"Health check failed: {exc}")

    if st.button("Run ingest", use_container_width=True):
        with st.spinner("Ingesting documents..."):
            try:
                resp = requests.post(
                    f"{api_base}/v1/ingest",
                    headers=_headers(),
                    timeout=300,
                )
                if resp.status_code >= 400:
                    st.error(resp.json().get("detail", resp.text))
                else:
                    st.success("Ingest complete")
                    st.json(resp.json())
            except requests.RequestException as exc:
                st.error(f"Ingest failed: {exc}")

# --- Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for i, src in enumerate(message["sources"], start=1):
                    meta = src.get("metadata") or {}
                    st.markdown(f"**[{i}]** `{meta.get('source', 'unknown')}`")
                    st.write(src.get("content", "")[:500])

if prompt := st.chat_input("Ask about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    f"{api_base}/v1/query",
                    headers=_headers(),
                    json={"question": prompt, "top_k": top_k},
                    timeout=120,
                )
                if resp.status_code >= 400:
                    answer = f"Error: {resp.json().get('detail', resp.text)}"
                    sources = []
                else:
                    payload = resp.json()
                    answer = payload.get("answer", "")
                    sources = payload.get("sources", [])
            except requests.RequestException as exc:
                answer = f"Could not reach API: {exc}"
                sources = []

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for i, src in enumerate(sources, start=1):
                    meta = src.get("metadata") or {}
                    st.markdown(f"**[{i}]** `{meta.get('source', 'unknown')}`")
                    st.write(src.get("content", "")[:500])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
