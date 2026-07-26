from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_core.documents import Document
import operator
from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------
# LLM
# ---------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini"
)

# ---------------------------------------
# Vector Memory
# ---------------------------------------

embeddings = OpenAIEmbeddings()

vector_db = Chroma(
    persist_directory="./memory_db",
    embedding_function=embeddings
)

# ---------------------------------------
# Store Long-Term Knowledge
# ---------------------------------------

vector_db.add_documents([
    Document(
        page_content="User likes Python and AI monitoring"
    )
])

# ---------------------------------------
# State
# ---------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# ---------------------------------------
# Node
# ---------------------------------------

def chatbot(state: AgentState):

    latest_message = state["messages"][-1].content

    # Retrieve long-term memory
    memories = vector_db.similarity_search(
        latest_message,
        k=2
    )

    memory_context = "\n".join([
        m.page_content for m in memories
    ])

    prompt = f"""
You are an AI assistant.

Long-term memory:
{memory_context}

User:
{latest_message}
"""

    response = llm.invoke(prompt)

    return {
        "messages": [response]
    }

# ---------------------------------------
# Graph
# ---------------------------------------

graph = StateGraph(AgentState)

graph.add_node("chatbot", chatbot)

graph.set_entry_point("chatbot")

graph.add_edge("chatbot", END)

# ---------------------------------------
# Checkpointer
# ---------------------------------------

memory = MemorySaver()

app = graph.compile(
    checkpointer=memory
)

# ---------------------------------------
# Thread Config
# ---------------------------------------

config = {
    "configurable": {
        "thread_id": "prem_session"
    }
}

# ---------------------------------------
# Chat
# ---------------------------------------

response = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="What technologies do I like?"
            )
        ]
    },
    config=config
)

print(response["messages"][-1].content)