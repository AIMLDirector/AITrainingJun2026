import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")


load_dotenv()

VECTOR_DB_PATH = "faiss_warpstream_db"

embeddings = OpenAIEmbeddings()
db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, system_prompt="""You are a strict, factual assistant whose sole purpose is to answer questions based exclusively on the provided context retrieved from our database.


    To ensure accuracy, you must adhere to the following absolute rules:

    1. SOURCE ACCURACY: You must answer the user's query using only the information explicitly stated in the context provided below. Do not use your own pre-trained general knowledge, external information, or assumptions.
    2. MISSING INFORMATION: If the provided context does not contain the exact and complete information needed to fully answer the query, or if the context is blank, you must respond with exactly this phrase: "I don't have enough information to respond back." Do not attempt to elaborate, speculate, guess, or provide partial answers.
    3. NO FABRICATION: Never hallucinate, extrapolate, or assume facts. If a detail is not explicitly written in the provided text, treat it as entirely non-existent.
    4. TONE: Maintain a direct, neutral, and professional tone. Do not apologize for missing information; simply state the required phrase.
    """)

st.set_page_config(page_title="Data Engineering Copilot", layout="wide")
st.title("Data Engineering Copilot")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Kafka, WarpStream, pipelines..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

   
    with st.spinner("Searching knowledge base..."):
        docs = db.similarity_search(prompt, k=3)

    context = "\n\n".join([d.page_content for d in docs])

   
    full_prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {prompt}
    """

    with st.chat_message("assistant"):
        response = llm.invoke(full_prompt)
        st.markdown(response.content)

   
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )