# from langchain_community.agent_toolkits.load_tools import load_huggingface_tool
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
DATA_DIR="../data/"


def load_documents(data_dir):
    docs = []

    for file in os.listdir(data_dir):

        path = os.path.join(data_dir, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())

        elif file.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())

        elif file.endswith(".csv"):
            loader = CSVLoader(path)
            docs.extend(loader.load())

    return docs


docs = load_documents(DATA_DIR)

# print(f"Loaded {len(docs)} documents")
# print(docs[0].page_content[:500])

# for doc in docs[:3]:
#     print(doc.metadata)

for doc in docs:
    print(doc.metadata)
