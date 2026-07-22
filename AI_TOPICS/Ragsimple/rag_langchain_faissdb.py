from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = "faiss_warpstream_db"

embeddings = OpenAIEmbeddings()
db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

st.set_page_config(page_title="knowledgebase article ", layout="wide")
st.title(" Date engineering Copilot")

while True:

    input_query = input("Enter your question: ")
    if input_query.lower() in ("exit", "quit"):
        break
    docs = db.similarity_search(input_query, k=2)
    print("\n--- AI Retrieved Knowledge ---\n")
    for i, d in enumerate(docs, 1):
        print(f"\n--- Result {i} ---\n")
        print(d.page_content)
