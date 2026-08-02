from typing import TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


# Define your state structure
class AgentState(TypedDict):
    query: str
    response: str


def research_agent(state):
    query = state["query"]
    result = llm.invoke(f"Research this topic: {query}")
    return {"response": result.content}


def coding_agent(state):
    # Using the research response as context for the coder
    context = state["response"]
    result = llm.invoke(
        f"Generate python code based on this research:\n\n{context}"
    )
    return {"response": result.content}


# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("research", research_agent)
workflow.add_node("coding", coding_agent)

workflow.set_entry_point("research")
workflow.add_edge("research", "coding")
workflow.add_edge("coding", END)

app = workflow.compile()

# Application loop
while True:
    user_input = input("Enter your query (or 'exit' to quit): ")
    if user_input.strip().lower() in ["exit", "quit"]:
        print("Exiting application. Goodbye!")
        break

    # Run the graph
    result = app.invoke({"query": user_input, "response": ""})

    # FIX: Access the correct key from your AgentState
    print("\n--- Final Output ---")
    print(result["response"])
    print("--------------------\n")
