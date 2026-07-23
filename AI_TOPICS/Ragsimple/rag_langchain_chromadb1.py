from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

CHROMA_DIR = "./chroma_db"


def build_vectordb():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    return Chroma(
        collection_name="books",
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )


def main():
    vectordb = build_vectordb()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    print("=" * 80)
    print("Knowledge Base Ready")
    print("=" * 80)

    while True:
        question = input("\nQuestion: ")

        if question.lower() in ("exit", "quit"):
            break

        results = vectordb.similarity_search_with_score(
            question,
            k=4,
        )

        print("\n" + "=" * 80)
        print("Retrieved Chunks")
        print("=" * 80)

        context = ""

        for idx, (doc, score) in enumerate(results, start=1):
            print(f"\nChunk {idx}")
            print("-" * 80)
            print(f"Similarity Score : {score}")
            print(f"Source           : {doc.metadata.get('source')}")
            print(f"Page             : {doc.metadata.get('page', 'N/A')}")
            print(f"Chunk ID         : {doc.metadata.get('chunk_id', 'N/A')}")
            print(f"Document Name    : {doc.metadata.get('document_name', 'N/A')}")

            print("\nContent Preview\n")
            print(doc.page_content[:500])

            context += doc.page_content + "\n\n"

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context, reply:
"I couldn't find the answer in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

        response = llm.invoke(prompt)

        print("\n" + "=" * 80)
        print("Answer")
        print("=" * 80)
        print(response.content)


if __name__ == "__main__":
    main()