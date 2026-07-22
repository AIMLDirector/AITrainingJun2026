import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# --------------------------------------------------
# Load environment
# --------------------------------------------------
load_dotenv()

VECTOR_DB_PATH = "faiss_warpstream_db"

# --------------------------------------------------
# Load embeddings & vector DB
# --------------------------------------------------
embeddings = OpenAIEmbeddings()

db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(page_title="Data Engineering Copilot", layout="wide")

st.title("Data Engineering Copilot")
st.caption("Semantic search over your knowledge base")

# --------------------------------------------------
# User input
# --------------------------------------------------
query = st.text_input(
    "Enter your question",
    placeholder="Ask something about Kafka, WarpStream, architecture...",
)

# --------------------------------------------------
# Search
# --------------------------------------------------
if query:
    with st.spinner("Searching knowledge base..."):
        docs = db.similarity_search(query, k=3)

    st.subheader("🔎 Retrieved Knowledge")

    for i, d in enumerate(docs, 1):
        with st.expander(f"Result {i}"):
            st.write(d.page_content)
