"""
Data Quality + Repair Pipeline with LLM
- Deterministic validation
- LLM analyzes issues and suggests repairs
- Human-in-the-loop approval
- Auto-applies approved repairs
"""

from typing import TypedDict, Annotated, Optional, Literal
from operator import add
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI          # or ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
load_dotenv()

# ============================================================
# 0. LLM Setup
# ============================================================
# Make sure you have OPENAI_API_KEY (or ANTHROPIC_API_KEY) set
llm = ChatOpenAI(
    model="gpt-4o-mini",          # change to gpt-4o / claude-3-5-sonnet etc.
    temperature=0
)

# ============================================================
# 1. State
# ============================================================
class DataState(TypedDict):
    job_id: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    quality_issues: Annotated[list[str], add]
    llm_analysis: Optional[str]
    llm_suggested_repairs: Optional[list[dict]]
    status: str
    human_decision: Optional[str]
    logs: Annotated[list[str], add]


def add_log(message: str) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"logs": [f"[{ts}] {message}"]}


# ============================================================
# 2. Nodes
# ============================================================
def validate_data(state: DataState) -> dict:
    """Deterministic quality checks"""
    issues = []
    for i, row in enumerate(state["raw_data"]):
        if not row.get("id"):
            issues.append(f"Row {i}: missing 'id'")
        if row.get("amount") is None:
            issues.append(f"Row {i}: missing 'amount'")
        elif not isinstance(row.get("amount"), (int, float)):
            issues.append(f"Row {i}: 'amount' is not numeric → {row.get('amount')}")
        elif row["amount"] < 0:
            issues.append(f"Row {i}: negative amount ({row['amount']})")
        if row.get("currency") and row["currency"] not in ("USD", "EUR", "INR"):
            issues.append(f"Row {i}: unsupported currency '{row['currency']}'")

    status = "clean" if not issues else "issues_found"
    return {
        "quality_issues": issues,
        "status": status,
        **add_log(f"Validation finished → {len(issues)} issue(s)")
    }


def llm_analyze(state: DataState) -> dict:
    """LLM reviews the issues and proposes concrete repairs"""
    if not state["quality_issues"]:
        return {
            "llm_analysis": "No issues found.",
            "llm_suggested_repairs": [],
            **add_log("LLM skipped – no issues")
        }

    system_prompt = """You are a senior data engineer.
Analyze the data quality issues and propose safe, concrete repairs.
Return ONLY valid JSON in this exact format:
{
  "analysis": "short explanation of the problems",
  "repairs": [
    {"row_index": 0, "field": "amount", "new_value": 0, "reason": "..."},
    ...
  ]
}
Be conservative. Prefer safe defaults (0 for missing amounts, USD for currency, etc.).
"""

    user_content = f"""Raw data sample:
{json.dumps(state["raw_data"][:8], indent=2)}

Quality issues detected:
{chr(10).join(state["quality_issues"])}
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ])

    try:
        # Extract JSON from the response
        content = response.content
        # simple cleanup if the model wraps it in ```json
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        parsed = json.loads(content.strip())
        analysis = parsed.get("analysis", "")
        repairs = parsed.get("repairs", [])
    except Exception as e:
        analysis = f"Failed to parse LLM response: {e}"
        repairs = []

    return {
        "llm_analysis": analysis,
        "llm_suggested_repairs": repairs,
        "status": "llm_analyzed",
        **add_log(f"LLM analysis complete – {len(repairs)} repair(s) suggested")
    }


def human_review(state: DataState) -> dict:
    """Pause for human approval of the LLM suggestions"""
    decision = interrupt({
        "job_id": state["job_id"],
        "message": "Please review LLM-suggested repairs",
        "issues": state["quality_issues"],
        "llm_analysis": state["llm_analysis"],
        "suggested_repairs": state["llm_suggested_repairs"],
        "options": ["approve", "reject", "edit"]   # edit can be handled later
    })
    return {
        "human_decision": decision,
        **add_log(f"Human decision → {decision}")
    }


def apply_repairs(state: DataState) -> dict:
    """Apply the LLM-suggested repairs (only if human approved)"""
    if state.get("human_decision") != "approve":
        return {
            "cleaned_data": state["raw_data"],
            "status": "rejected",
            **add_log("Repairs rejected by human – original data kept")
        }

    cleaned = [row.copy() for row in state["raw_data"]]
    applied = []

    for repair in state.get("llm_suggested_repairs", []):
        idx = repair.get("row_index")
        field = repair.get("field")
        new_val = repair.get("new_value")
        if idx is not None and 0 <= idx < len(cleaned) and field:
            old_val = cleaned[idx].get(field)
            cleaned[idx][field] = new_val
            applied.append(f"Row {idx}: {field} {old_val} → {new_val}")

    return {
        "cleaned_data": cleaned,
        "status": "completed",
        "quality_issues": applied,          # reuse field to show what was done
        **add_log(f"Applied {len(applied)} repair(s)")
    }


def finalize(state: DataState) -> dict:
    if state["status"] == "clean":
        return {
            "cleaned_data": state["raw_data"],
            "status": "completed",
            **add_log("Data was already clean – nothing to do")
        }
    return add_log("Pipeline finished")


# ============================================================
# 3. Routing
# ============================================================
def after_validate(state: DataState) -> Literal["llm_analyze", "finalize"]:
    return "llm_analyze" if state["quality_issues"] else "finalize"


def after_human(state: DataState) -> Literal["apply_repairs", "finalize"]:
    return "apply_repairs" if state.get("human_decision") == "approve" else "finalize"


# ============================================================
# 4. Build Graph
# ============================================================
builder = StateGraph(DataState)

builder.add_node("validate", validate_data)
builder.add_node("llm_analyze", llm_analyze)
builder.add_node("human_review", human_review)
builder.add_node("apply_repairs", apply_repairs)
builder.add_node("finalize", finalize)

builder.add_edge(START, "validate")
builder.add_conditional_edges("validate", after_validate)
builder.add_edge("llm_analyze", "human_review")
builder.add_conditional_edges("human_review", after_human)
builder.add_edge("apply_repairs", "finalize")
builder.add_edge("finalize", END)

checkpointer = MemorySaver()
pipeline = builder.compile(checkpointer=checkpointer)


# ============================================================
# 5. Example Run
# ============================================================
if __name__ == "__main__":
    sample_data = [
        {"id": "TX001", "amount": 150.0, "currency": "USD"},
        {"id": "TX002", "amount": None,  "currency": "EUR"},
        {"id": "TX003", "amount": -42.5, "currency": "USD"},
        {"id": None,    "amount": 99.0,  "currency": "INR"},
        {"id": "TX005", "amount": 200,   "currency": "GBP"},
        {"id": "TX006", "amount": 75.5,  "currency": "USD"},
    ]

    config = {"configurable": {"thread_id": "dq-llm-001"}}

    print("=" * 70)
    print("STEP 1 – Run until human review (interrupt)")
    print("=" * 70)

    # First invoke – will stop at human_review
    pipeline.invoke(
        {
            "job_id": "dq-llm-001",
            "raw_data": sample_data,
            "cleaned_data": [],
            "quality_issues": [],
            "llm_analysis": None,
            "llm_suggested_repairs": None,
            "status": "pending",
            "human_decision": None,
            "logs": []
        },
        config=config
    )

    state = pipeline.get_state(config).values
    print("\nStatus:", state["status"])
    print("\nLLM Analysis:\n", state.get("llm_analysis"))
    print("\nSuggested repairs:")
    print(json.dumps(state.get("llm_suggested_repairs", []), indent=2))
    print("\nLogs:")
    for line in state["logs"]:
        print(" ", line)

    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("STEP 2 – Human approves the LLM suggestions")
    print("=" * 70)

    # Resume with human decision
    pipeline.invoke(Command(resume="approve"), config=config)

    final = pipeline.get_state(config).values
    print("\nFinal status:", final["status"])
    print("\nCleaned data:")
    print(json.dumps(final.get("cleaned_data", []), indent=2))
    print("\nFull logs:")
    for line in final["logs"]:
        print(" ", line)