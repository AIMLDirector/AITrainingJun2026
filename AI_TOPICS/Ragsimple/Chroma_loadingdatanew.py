import os
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_docling.loader import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from docling.datamodel.pipeline_options import PdfPipelineOptions
load_dotenv()
pipeline_options = PdfPipelineOptions()
pipeline_options.allow_external_plugins = True
DATA_DIR = "../data"
CHROMA_DIR = "./chroma_db"


def load_documents():
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            loader = DoclingLoader(path,pipeline_options=pipeline_options)
            docs.extend(loader.load())
    return docs

def main():
    docs = load_documents()
    print(f"Loaded {len(docs)} pages")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for d in tqdm(docs, desc="splitting"):
        chunks.extend(splitter.split_documents([d]))

    print(f"Created {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings()
    db_name = CHROMA_DIR

    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=db_name
    )
    print(f"Vectorstore created with {vectorstore._collection.count()} documents")
    collection = vectorstore._collection
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"The vectors have {dimensions:,} dimensions")


if __name__ == "__main__":
    main()
