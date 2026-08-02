"""
Data Quality + Repair Pipeline using LangGraph
- Validates data
- Auto-repairs simple issues
- Escalates complex issues to human via interrupt()
- Supports resume after human decision
"""

from typing import TypedDict, Annotated, Literal, Optional
from operator import add
import json
from datetime import datetime
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
load_dotenv()

# ============================================================
# 1. State Definition
# ============================================================
class DataState(TypedDict):
    job_id: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    quality_issues: Annotated[list[str], add]
    status: str                          # pending | validated | repaired | needs_human | completed | rejected
    human_decision: Optional[str]        # approve_repair | reject | manual_fix
    logs: Annotated[list[str], add]


def log(state: DataState, message: str) -> dict:
    """Helper to append timestamped log entries"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"logs": [f"[{timestamp}] {message}"]}


# ============================================================
# 2. Nodes
# ============================================================
def validate_data(state: DataState) -> dict:
    """Check for common data quality problems"""
    issues = []
    raw = state["raw_data"]

    for i, row in enumerate(raw):
        if not row.get("id"):
            issues.append(f"Row {i}: missing 'id'")
        if row.get("amount") is None:
            issues.append(f"Row {i}: missing 'amount'")
        elif not isinstance(row.get("amount"), (int, float)):
            issues.append(f"Row {i}: 'amount' is not numeric")
        elif row.get("amount") < 0:
            issues.append(f"Row {i}: negative amount ({row['amount']})")

        if row.get("currency") and row["currency"] not in ("USD", "EUR", "INR"):
            issues.append(f"Row {i}: unsupported currency '{row['currency']}'")

    status = "validated" if not issues else "needs_review"

    updates = {
        "quality_issues": issues,
        "status": status,
        **log(state, f"Validation complete. Found {len(issues)} issue(s). Status → {status}")
    }
    return updates


def auto_repair(state: DataState) -> dict:
    """Automatically fix simple, safe issues"""
    cleaned = []
    repairs_made = []

    for i, row in enumerate(state["raw_data"]):
        fixed = row.copy()

        # Fill missing amount with 0
        if fixed.get("amount") is None:
            fixed["amount"] = 0
            repairs_made.append(f"Row {i}: set missing amount → 0")

        # Convert negative amounts to absolute value
        if isinstance(fixed.get("amount"), (int, float)) and fixed["amount"] < 0:
            original = fixed["amount"]
            fixed["amount"] = abs(fixed["amount"])
            repairs_made.append(f"Row {i}: converted negative amount {original} → {fixed['amount']}")

        # Default currency
        if not fixed.get("currency"):
            fixed["currency"] = "USD"
            repairs_made.append(f"Row {i}: set missing currency → USD")

        cleaned.append(fixed)

    return {
        "cleaned_data": cleaned,
        "status": "repaired",
        "quality_issues": repairs_made,          # reuse field to show what was fixed
        **log(state, f"Auto-repair finished. {len(repairs_made)} fix(es) applied.")
    }


def human_review(state: DataState) -> dict:
    """
    Pause the graph and wait for human decision.
    The interrupt payload is what the human sees.
    """
    decision = interrupt({
        "job_id": state["job_id"],
        "message": "Data quality issues require human review",
        "issue_count": len(state["quality_issues"]),
        "issues": state["quality_issues"],
        "sample_raw_data": state["raw_data"][:5],
        "options": ["approve_repair", "reject", "manual_fix"]
    })

    return {
        "human_decision": decision,
        **log(state, f"Human decision received → {decision}")
    }


def finalize(state: DataState) -> dict:
    """Final node – prepare clean output"""
    if state.get("human_decision") == "reject":
        return {
            "status": "rejected",
            "cleaned_data": [],
            **log(state, "Job rejected by human. No data published.")
        }

    # If we came from auto_repair or human approved repair
    cleaned = state.get("cleaned_data") or state["raw_data"]
    return {
        "cleaned_data": cleaned,
        "status": "completed",
        **log(state, f"Pipeline completed successfully. {len(cleaned)} rows ready.")
    }


# ============================================================
# 3. Routing Logic
# ============================================================
def route_after_validation(state: DataState) -> Literal["auto_repair", "human_review", "finalize"]:
    issues = state.get("quality_issues", [])
    if not issues:
        return "finalize"           # clean data → done
    if len(issues) <= 3:
        return "auto_repair"        # few simple issues → auto fix
    return "human_review"           # many / complex issues → human


def route_after_human(state: DataState) -> Literal["auto_repair", "finalize"]:
    decision = state.get("human_decision")
    if decision == "approve_repair":
        return "auto_repair"
    # reject or manual_fix both go to finalize
    return "finalize"


# ============================================================
# 4. Build the Graph
# ============================================================
builder = StateGraph(DataState)

builder.add_node("validate", validate_data)
builder.add_node("auto_repair", auto_repair)
builder.add_node("human_review", human_review)
builder.add_node("finalize", finalize)

builder.add_edge(START, "validate")
builder.add_conditional_edges("validate", route_after_validation)
builder.add_edge("auto_repair", "finalize")
builder.add_conditional_edges("human_review", route_after_human)
builder.add_edge("finalize", END)

# Persistence is required for interrupt / resume
checkpointer = MemorySaver()
pipeline = builder.compile(checkpointer=checkpointer)


# ============================================================
# 5. Sample Run + Logs
# ============================================================
if __name__ == "__main__":
    # Sample dirty data
    sample_data = [
        {"id": "TX001", "amount": 150.0, "currency": "USD"},
        {"id": "TX002", "amount": None, "currency": "EUR"},          # missing amount
        {"id": "TX003", "amount": -42.5, "currency": "USD"},         # negative
        {"id": None,    "amount": 99.0,  "currency": "INR"},         # missing id
        {"id": "TX005", "amount": 200,   "currency": "GBP"},         # unsupported currency
        {"id": "TX006", "amount": 75.5,  "currency": "USD"},
    ]

    config = {"configurable": {"thread_id": "dq-job-2026-08-02-001"}}

    print("=" * 70)
    print("STEP 1: First invoke (will pause if human review is needed)")
    print("=" * 70)

    result = pipeline.invoke(
        {
            "job_id": "dq-job-2026-08-02-001",
            "raw_data": sample_data,
            "cleaned_data": [],
            "quality_issues": [],
            "status": "pending",
            "human_decision": None,
            "logs": []
        },
        config=config
    )

    # When an interrupt happens, LangGraph raises an exception or returns
    # a special state. In recent versions you typically check the state.
    state = pipeline.get_state(config)
    print("\nCurrent status:", state.values.get("status"))
    print("\n--- Pipeline Logs so far ---")
    for entry in state.values.get("logs", []):
        print(entry)

    print("\nQuality issues found:")
    for issue in state.values.get("quality_issues", []):
        print(" •", issue)

    # --------------------------------------------------------
    # Simulate human decision (in real systems this comes from UI / API)
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("STEP 2: Human reviews and chooses 'approve_repair'")
    print("=" * 70)

    # Resume the graph with the human decision
    resumed = pipeline.invoke(
        Command(resume="approve_repair"),
        config=config
    )

    final_state = pipeline.get_state(config).values

    print("\n--- Final Logs ---")
    for entry in final_state.get("logs", []):
        print(entry)

    print("\nFinal status:", final_state.get("status"))
    print("Human decision:", final_state.get("human_decision"))
    print("\nCleaned data preview:")
    print(json.dumps(final_state.get("cleaned_data", [])[:4], indent=2))