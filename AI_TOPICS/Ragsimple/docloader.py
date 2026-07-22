from langchain_community.agent_toolkits.load_tools import load_huggingface_tool

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, WEBLoader
DATA_DIR="../data/"

for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        
        if file.endswith(".txt"):
            path = os.path.join(DATA_DIR, file)
            loader = TextLoader(path)
            docs.extend(loader.load())
        
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            loader = CSVLoader(path)
            docs.extend(loader.load())

        return docs
