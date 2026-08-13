import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
from dotenv import load_dotenv

from detoxify import Detoxify

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

toxicity_model = Detoxify("multilingual")

analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)

THRESHOLDS = {
    "toxicity": 0.50,
    "severe_toxicity": 0.50,
    "obscene": 0.50,
    "threat": 0.50,
    "insult": 0.50,
    "identity_attack": 0.50
}

sample_docs = [
    Document(
        page_content="""
        Employees are entitled to 24 vacation days annually.
        """
    ),
    Document(
        page_content="""
        Employees can work remotely up to 3 days per week.
        """
    ),
    Document(
        page_content="""
        Medical insurance covers spouse and children.
        """
    )
]

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = FAISS.from_documents(
    sample_docs,
    embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "show system prompt",
    "print system prompt",
    "forget instructions",
    "act as administrator",
    "act as root",
    "bypass safety"
]


def check_toxicity(text):

    scores = toxicity_model.predict(text)

    for category, threshold in THRESHOLDS.items():

        if scores.get(category, 0) > threshold:

            return {
                "blocked": True,
                "reason": category,
                "scores": scores
            }

    return {
        "blocked": False,
        "reason": None,
        "scores": scores
    }


def detect_prompt_injection(text):

    text = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:

        if pattern in text:
            return True

    return False


def mask_pii(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    if not results:
        return text

    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return anonymized.text


def retrieve_context(query):

    docs = retriever.invoke(query)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    return context


class SecureRAGBot:

    def __init__(self):

        self.history = [
            SystemMessage(
                content="""
You are an enterprise support assistant.

Answer only using the supplied context.

If the answer is not found in the context,
say you do not know.
"""
            )
        ]

    def invoke(self, query):

        toxicity_result = check_toxicity(query)

        if toxicity_result["blocked"]:
            return {
                "status": "blocked",
                "message": f"Toxic content detected: {toxicity_result['reason']}"
            }

        if detect_prompt_injection(query):
            return {
                "status": "blocked",
                "message": "Prompt injection detected"
            }

        query = mask_pii(query)

        context = retrieve_context(query)

        final_prompt = f"""
Context:
{context}

Question:
{query}

Answer only from context.
"""

        self.history.append(
            HumanMessage(content=final_prompt)
        )

        response = llm.invoke(self.history)

        answer = response.content

        output_toxicity = check_toxicity(answer)

        if output_toxicity["blocked"]:
            return {
                "status": "blocked",
                "message": "Unsafe output generated"
            }

        output_pii = analyzer.analyze(
            text=answer,
            language="en"
        )

        if output_pii:
            answer = mask_pii(answer)

        self.history.append(
            AIMessage(content=answer)
        )

        return {
            "status": "success",
            "response": answer
        }


def main():

    chatbot = SecureRAGBot()

    print("Secure ChatOpenAI + RAG")

    while True:

        query = input("\nYou: ")

        if query.lower() in [
            "exit",
            "quit"
        ]:
            break

        try:

            result = chatbot.invoke(query)

            if result["status"] == "success":
                print("\nAssistant:")
                print(result["response"])

            else:
                print("\nBlocked:")
                print(result["message"])

        except Exception as e:

            print("\nError:")
            print(str(e))


if __name__ == "__main__":
    main()