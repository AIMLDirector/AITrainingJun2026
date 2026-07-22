from tqdm import tqdm
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    WebBaseLoader, UnstructuredPowerPointLoader
)
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
# --------------------------------------------------
# 1️⃣ Load documents
# --------------------------------------------------
docs = []

docs.extend(TextLoader("../data/requirement.txt").load())
docs.extend(PyPDFLoader("../data/LLMarchitecture.pdf").load())
docs.extend(CSVLoader("../data/bigmac.csv").load())
docs.extend(
    WebBaseLoader(
        "https://www.warpstream.com/blog/zero-disks-is-better-for-kafka"
    ).load()
)

print(f"Total raw documents loaded: {len(docs)}")
# print(docs)

# --------------------------------------------------
# 2️⃣ Split documents into chunks
# --------------------------------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)  # chunk size = 500  tokens is roughly 3750 characters, with 50 tokens (375 chars) overlap

# Tqdm for iteration and progress bar visualization, data cleanup, and debugging purposes
# range(len(docs)) -> tqdm(docs) for better readability and progress tracking

chunks = []
for doc in tqdm(docs, desc="Splitting documents"):
    chunks.extend(text_splitter.split_documents([doc]))

print(f"Total chunks created: {len(chunks)}")
print(chunks[10:20])

# --------------------------------------------------
# 3️⃣ Create embeddings & FAISS vector store
# --------------------------------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings,
)  # it will be in system memory

# (Optional) persist index
vectorstore.save_local("faiss_index")


retriever = vectorstore.as_retriever(search_kwargs={"k": 6})


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are an assistant answering questions using ONLY the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{question}
""")


def ask(question: str):
    docs = retriever.invoke(question)

    context = "\n\n".join(d.page_content for d in docs)

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )
    return response.content


if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break

        answer = ask(q)
        print("\nAnswer:\n", answer)
