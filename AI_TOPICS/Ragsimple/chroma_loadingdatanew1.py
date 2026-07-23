import os
from dotenv import load_dotenv
from tqdm import tqdm
from langchain_docling.loader import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DATA_DIR = "../data"
CHROMA_DIR = "./chroma_db"


def load_documents():
    docs = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = DoclingLoader(os.path.join(DATA_DIR, file))
            documents = loader.load()

            # Keep only simple metadata
            for doc in documents:
                doc.metadata = {
                    "source": file
                }

            docs.extend(documents)

    return docs


def main():

    # Load PDFs
    docs = load_documents()
    print(f"Loaded {len(docs)} pages")

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(docs)

    print(f"Created {len(chunks)} chunks")

    # OpenAI Embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Create Chroma DB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="books",
    )

    print(f"Stored {vectorstore._collection.count()} chunks")


if __name__ == "__main__":
    main()