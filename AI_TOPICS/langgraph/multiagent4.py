import os
from typing import Literal, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Define state to track logs and agent assignments
class LogState(TypedDict):
    log_line: str
    severity: str
    critical_analysis: str
    warning_analysis: str


# Node 1: Router Agent (Classifies the severity)
def log_router_agent(state: LogState):
    log_line = state["log_line"]

    prompt = f"""
    Analyze this CloudWatch log line and classify its severity.
    You must choose exactly one of these labels: CRITICAL, WARNING, ERROR, or INFO.
    
    Log line: {log_line}
    
    Respond with ONLY the single word label.
    """
    response = llm.invoke(prompt).content.strip().upper()

    # Fallback safety
    if response not in ["CRITICAL", "WARNING", "ERROR", "INFO"]:
        response = "INFO"

    return {"severity": response}


# Node 2: Critical Agent (Handles CRITICAL logs)
def critical_agent(state: LogState):
    log_line = state["log_line"]
    prompt = f"CRITICAL INCIDENT DETECTED. Provide an immediate root cause analysis and mitigation steps for this log: {log_line}"
    response = llm.invoke(prompt)
    return {"critical_analysis": response.content}


# Node 3: Warning/Error Agent (Handles WARNING and ERROR logs)
def warning_error_agent(state: LogState):
    log_line = state["log_line"]
    prompt = f"Issue detected. Provide troubleshooting advice or standard fixes for this log: {log_line}"
    response = llm.invoke(prompt)
    return {"warning_analysis": response.content}


# Routing logic function for conditional edges
def route_based_on_severity(
    state: LogState,
) -> Literal["critical_node", "warning_node", "end"]:
    severity = state["severity"]

    if severity == "CRITICAL":
        return "critical_node"
    elif severity in ["WARNING", "ERROR"]:
        return "warning_node"
    else:
        return "end"  # Skip INFO logs


# Build the Graph
workflow = StateGraph(LogState)

# Add Nodes
workflow.add_node("router", log_router_agent)
workflow.add_node("critical_node", critical_agent)
workflow.add_node("warning_node", warning_error_agent)

# Set Entry Point
workflow.set_entry_point("router")

# Add Conditional Routing
workflow.add_conditional_edges(
    "router",
    route_based_on_severity,
    {
        "critical_node": "critical_node",
        "warning_node": "warning_node",
        "end": END,
    },
)

# Connect processing nodes to the end
workflow.add_edge("critical_node", END)
workflow.add_edge("warning_node", END)

# Compile Application
app = workflow.compile()

# --- Execution Simulation ---

# Simulated CloudWatch log file data
mock_cloudwatch_logs = [
    '2026-05-30T10:00:00Z [INFO] User "john_doe" logged in successfully.',
    "2026-05-30T10:01:15Z [WARNING] Disk space utilization is at 88% on volume vol-01234abc.",
    "2026-05-30T10:02:30Z [ERROR] Failed to connect to Redis cache cluster. Connection timed out.",
    "2026-05-30T10:05:00Z [CRITICAL] Core database primary node is down! Split-brain scenario detected. Data corruption imminent.",
]

print("Starting CloudWatch Log File Analysis...\n")

for line in mock_cloudwatch_logs:
    print(f"Reading Log: {line}")

    # Initialize state for this log line
    initial_state = {
        "log_line": line,
        "severity": "",
        "critical_analysis": "",
        "warning_analysis": "",
    }

    # Execute workflow
    result = app.invoke(initial_state)

    # Display results based on how it routed
    severity = result["severity"]
    print(f"-> Router classified as: {severity}")

    if severity == "CRITICAL":
        print(f"🚨 [CRITICAL AGENT OUTPUT]:\n{result['critical_analysis']}\n")
    elif severity in ["WARNING", "ERROR"]:
        print(f"⚠️ [WARNING/ERROR AGENT OUTPUT]:\n{result['warning_analysis']}\n")
    else:
        print("ℹ️ [INFO]: Log ignored. No action required.\n")

    print("-" * 60)
