from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
)

from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate

from langchain_classic.chains import (
    create_retrieval_chain
)

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)
from dotenv import load_dotenv
load_dotenv()

def build_rag(pdf_path):

    # Load PDF
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    splits = splitter.split_documents(documents)

    # Embeddings
    embeddings = OpenAIEmbeddings()

    # Vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    retriever = vectorstore.as_retriever()

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the provided context.

        Context:
        {context}

        Question:
        {input}
        """
    )

    # Create document chain
    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    # Create retrieval chain
    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain