import operator
import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

# Load API keys from your .env file
load_dotenv()

# ---------------------------------------
# 1. Initialize LLM & Vector Database
# ---------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings()

vector_db = Chroma(
    persist_directory="./memory_db", 
    embedding_function=embeddings
)

# ---------------------------------------
# 2. Seed Long-Term Memory (10 Lines)
# ---------------------------------------
# Clearing existing collection to ensure clean verification setup
try:
    vector_db.delete_collection()
    vector_db = Chroma(persist_directory="./memory_db", embedding_function=embeddings)
except Exception:
    pass

sample_memories = [
    "The user expressed a strong preference for using Python as their primary programming language for all back-end engineering and has a keen professional interest in AI system monitoring frameworks.",
    "Project requirements state that the core infrastructure must be built using Python microservices, leveraging automated AI monitoring tools to track model drift and latency in production environments.",
    "When building data pipelines, the developer relies heavily on Python's ecosystem, specifically integrating OpenTelemetry and specialized AI monitoring dashboards to observe LLM performance analytics.",
    "An entry in the architectural logs indicates that the team uses Python-based MLOps workflows to deploy models, emphasizing real-time AI monitoring to catch data anomalies early.",
    "The user prefers setting up automated alert thresholds using Python scripts that interface with enterprise AI monitoring platforms to track token usage, api costs, and error rates.",
    "A note from the developer onboarding session confirms that the engineer builds applications exclusively with Python and is currently evaluating modern AI monitoring stacks for production guards.",
    "The engineer's workflow revolves around profiling Python code optimization alongside comprehensive AI monitoring metrics to ensure high throughput and low-latency inferences.",
    "To prevent hallucination and secure application outputs, the user configures validation guardrails inside Python applications combined with continuous AI monitoring and evaluation tools.",
    "The local development profile specifies a Python 3.11 environment integrated with deep-learning libraries and native hooks for upstream AI monitoring and tracing engines.",
    "According to past user requests, the preferred system design features a Python FastAPI backend connected to an interactive telemetry interface dedicated entirely to deep-dive AI monitoring."
]

# Convert strings into LangChain Document instances and batch add them
documents = [Document(page_content=line) for line in sample_memories]
vector_db.add_documents(documents)

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

def chatbot(state: AgentState):
    latest_message = state["messages"][-1].content

    # Query Chroma for the top 2 matching long-term memories
    memories = vector_db.similarity_search(latest_message, k=2)

    # VISUAL VERIFICATION LOG: See vector data extraction live
    print("\n[VECTOR DB MATCHES RETRIEVED]")
    if not memories:
        print("No matching long-term memory found.")
    for idx, doc in enumerate(memories):
        print(f"   [{idx + 1}] {doc.page_content}")
    print("-" * 50)

    # Format retrieved items into context
    memory_context = "\n".join([m.page_content for m in memories])

    prompt = f"""
You are an AI assistant. Use the long-term memory context provided below to personalize your interactions, but keep your responses natural and highly conversational. Do not mention that you read this from a log file or memory database unless asked.

Long-term memory context:
{memory_context}

User:
{latest_message}
"""
    response = llm.invoke(prompt)
    return {"messages": [response]}

# ---------------------------------------
# 4. Assemble and Compile LangGraph
# ---------------------------------------
graph = StateGraph(AgentState)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

# MemorySaver handles short-term conversation thread memory
short_term_memory = MemorySaver()
app = graph.compile(checkpointer=short_term_memory)

# Configure a unique execution thread session
config = {"configurable": {"thread_id": "interactive_verification_session"}}

print(" System Initialized. Long-term memory seeded.")
print("Type 'exit' or 'quit' to terminate the session.\n")

while True:
    try:
        user_input = input("You: ")
        
        # Termination check
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Ending session. Goodbye!")
            break
            
        # Ignore accidental empty returns
        if not user_input.strip():
            continue

        # Execute processing step inside LangGraph
        response = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )

        # Print out the final response from our conversational graph state
        print(f"Bot: {response['messages'][-1].content}\n")

    except KeyboardInterrupt:
        print("\nSession interrupted.")
        break



#What should we look out for regarding model performance in production?
#what stack do I use for data pipelines?
