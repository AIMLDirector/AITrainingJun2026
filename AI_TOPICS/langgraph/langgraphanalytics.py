import json
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()


class IncidentState(TypedDict):
    """Tracks state and inputs through the LangGraph engine."""
    messages: Annotated[list[BaseMessage], add_messages]
    java_log: str
    infra_log: str
    network_log: str
    root_cause: str
    short_term_solution: str
    long_term_solution: str


class RootCauseAnalysis(BaseModel):
    """Strict schema for data isolation during parsing."""
    root_cause: str = Field(
        description="The exact root cause derived deterministically from log timelines."
    )
    affected_components: list[str] = Field(
        description="List of systems impacted by this failure."
    )


class MitigationStrategy(BaseModel):
    """Strict schema for remediation tracking."""
    short_term_fix: str = Field(
        description="Immediate tactical step to restore system health."
    )
    long_term_fix: str = Field(
        description="Strategic engineering changes to prevent recurrence permanently."
    )



def analyzer_agent(state: IncidentState):
    """Reviews logs and isolates the core failure vector."""
    # Temperature 0.0 guarantees token selection reproducibility 
    llm = ChatOpenAI(model="gpt-5.5", temperature=0.0)
    structured_llm = llm.with_structured_output(RootCauseAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a Senior Site Reliability Engineer. Analyze the application, infrastructure, "
            "and network logs to identify the single root cause. Do not guess; stick strictly to the logs.\n\n"
            "Java Log:\n{java_log}\n\n"
            "Infra Log:\n{infra_log}\n\n"
            "Network Log:\n{network_log}"
        ),
        ("human", "Determine the root cause based on cross-referencing these logs.")
    ])

    chain = prompt | structured_llm
    result = chain.invoke({
        "java_log": state["java_log"],
        "infra_log": state["infra_log"],
        "network_log": state["network_log"]
    })

    return {"root_cause": result.root_cause}


def solution_agent(state: IncidentState):
    """Provides actionable short and long-term resolutions based only on the isolated root cause."""
    llm = ChatOpenAI(model="gpt-5.5", temperature=0.0)
    structured_llm = llm.with_structured_output(MitigationStrategy)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a Principal Software Architect. Given the validated root cause of an incident, "
            "provide a short-term tactical mitigation and a long-term architectural resolution."
        ),
        ("human", "Root Cause: {root_cause}")
    ])

    chain = prompt | structured_llm
    result = chain.invoke({"root_cause": state["root_cause"]})

    return {
        "short_term_solution": result.short_term_fix,
        "long_term_solution": result.long_term_fix
    }


def summary_node(state: IncidentState):
    """Compiles the telemetry metrics and output states into a final human-readable report."""
    report = (
        f"###  Root Cause Analysis\n{state['root_cause']}\n\n"
        f"### Short-Term Solution\n{state['short_term_solution']}\n\n"
        f"### Long-Term Solution\n{state['long_term_solution']}"
    )
    return {"messages": [AIMessage(content=report)]}


workflow = StateGraph(IncidentState)

# Register execution agents
workflow.add_node("analyzer_agent", analyzer_agent)
workflow.add_node("solution_agent", solution_agent)
workflow.add_node("summary_node", summary_node)

# Linear, predictable evaluation sequence
workflow.add_edge(START, "analyzer_agent")
workflow.add_edge("analyzer_agent", "solution_agent")
workflow.add_edge("solution_agent", "summary_node")
workflow.add_edge("summary_node", END)

# Compile graph
app = workflow.compile()


# ==========================================
# 5. TEST RUN
# ==========================================
if __name__ == "__main__":
    inputs = {
        "messages": [HumanMessage(content="Process logs")],
        "java_log": "2026-07-02 20:30:05 [WARN] c.z.h.HikariPool: Connection leak detection triggered for connection conn0: user active 60000ms.",
        "infra_log": "2026-07-02 20:30:00 [INFO] kernel: oom-kill event skipped. Memory margin stable at 12%.",
        "network_log": "2026-07-02 20:29:50 [INFO] firewall: Allowed outbound connections to database-primary:5432.",
        "root_cause": "",
        "short_term_solution": "",
        "long_term_solution": ""
    }

    output = app.invoke(inputs)
    print(output["messages"][-1].content)
