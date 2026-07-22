from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
load_dotenv()


chroma_dir = "./chroma_db"
openai_embeddings = OpenAIEmbeddings()


def chat_query():
    print("Welcome to the Data Engineering Copilot!")


def main(user_query: str)-> str:
    print("User query:", user_query)


if __name__ == "__main__":
    while True:
        user_query = input("Enter your question (or type 'exit' to quit): ")
        if user_query.lower() in ("exit", "quit"):
            break
        response = main(user_query)
        output = response.content if hasattr(response, "content") else str(response)
        print("\nAnswer:\n", output)


# Retriever 
#static retriever -- question -> embedding -> search in vector db(doc) -> retrieve relevant docs
#dynamic retriever -- question ->embedding --> search in elasticsearch(-1 hours) - livestream data(logs) -> retrieve relevant docs

#hybrid retriever - question -- search in db and elasticsearch ->summarize the anwser->  retrieve relevant docs

#what is the error creating in last one hour on kafka topic warpstream-logs and provide me the suggestion to fix this error
