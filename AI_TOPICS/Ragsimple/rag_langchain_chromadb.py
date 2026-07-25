# rag_langchain.py
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA

# RAG - Retrieve /augment /generate 
CHROMA_DIR = "./chroma_db"


def build_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = Chroma(
        collection_name="books",
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )
    return vectordb.as_retriever(search_kwargs={"k": 4})


def main():
    retriever = build_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # updto 2024

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )

    print("Ready — ask questions about your PDFs. Type 'exit' to quit.")
    while True:
        q = input("Q: ")
        if q.lower() in ("exit", "quit"):
            break
        resp = qa.invoke(q)
        print("A:", resp)


if __name__ == "__main__":
    main()

#model invoke -> retrieve - > ( llm model(4 answer - > summarize text the matching information using system prompt), chromadb( vector number - 4 answer), embedding( question - vector number) )
