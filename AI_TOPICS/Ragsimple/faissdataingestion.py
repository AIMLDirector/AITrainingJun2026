from dotenv import load_dotenv
from tqdm import tqdm

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    WebBaseLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

VECTOR_DB_PATH = "faiss_warpstream_db"


loaders = [
    TextLoader("../data/requirement.txt"),
    PyPDFLoader("../data/LLMarchitecture.pdf"),
    CSVLoader("../data/bigmac.csv"),
    WebBaseLoader("https://www.warpstream.com/blog/zero-disks-is-better-for-kafka"),
]

documents = []
for loader in loaders:
    documents.extend(loader.load())

print(f"\nLoaded {len(documents)} raw documents")

# print(documents)

# -------------------------------------------------------
# SPLIT INTO CHUNKS
# -------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, chunk_overlap=100, separators=["\n\n", "\n", ".", " ", ""]
)

chunks = splitter.split_documents(documents)

print(chunks[1:10])

# Clean garbage characters
for c in chunks:
    c.page_content = c.page_content.replace("\x00", "").strip()

print(f"Created {len(chunks)} chunks")


embeddings = OpenAIEmbeddings()

db = None
batch_size = 50

for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding"):
    batch = chunks[i : i + batch_size]

    if db is None:
        db = FAISS.from_documents(batch, embeddings)
    else:
        db.add_documents(batch)

print("Vectorization completed")
db.save_local(VECTOR_DB_PATH)
print(f"\nFAISS Vector DB saved at: {VECTOR_DB_PATH}")
