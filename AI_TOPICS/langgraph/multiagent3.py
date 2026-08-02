from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


# Updated state to hold both outputs separately
class AgentState(TypedDict):
    query: str
    research_data: str
    code_data: str


def research_agent(state):
    query = state["query"]
    result = llm.invoke(f"Research this topic: {query}")
    # Save specifically to research_data
    return {"research_data": result.content}


def coding_agent(state):
    query = state["query"]
    research = state["research_data"]
    result = llm.invoke(
        f"Generate python code for: {query}. Use this research context: {research}"
    )
    # Save specifically to code_data
    return {"code_data": result.content}


workflow = StateGraph(AgentState)
workflow.add_node("research", research_agent)
workflow.add_node("coding", coding_agent)

workflow.set_entry_point("research")
workflow.add_edge("research", "coding")
workflow.add_edge("coding", END)

app = workflow.compile()

while True:
    user_input = input("Enter your query (or 'exit' to quit): ")
    if user_input.strip().lower() in ["exit", "quit"]:
        print("Exiting application. Goodbye!")
        break

    # Initialize the state keys
    result = app.invoke(
        {"query": user_input, "research_data": "", "code_data": ""}
    )

    # Print both responses clearly
    print("\n================ RESEARCH AGENT ================")
    print(result["research_data"])

    print("\n================ CODING AGENT ==================")
    print(result["code_data"])
    print("================================================\n")
