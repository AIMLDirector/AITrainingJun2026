from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()

class Kafkalogstate(TypedDict):
    raw_log : str
    extracted_info : str
    root_cause : str

llm = ChatOpenAI(model="gpt-4o-mini")

def log_extraction(state:Kafkalogstate) -> dict:
    """Filter out noises and extract critical error patterns from kakfa logs"""
    prompt = f"""You are a log analyst. Your task is to analyze the following Kafka log and extract critical error patterns, including error messages, timestamps, and any relevant context."
    f"Here is the Kafka log:\n{state['raw_log']}\nPlease provide a structured summary of the critical error patterns you find."""

    reponse = llm.invoke(prompt)
    return {"extracted_info": reponse.content}


def root_cause_analysis(state:Kafkalogstate) -> dict:
    """Analyze the extracted information to identify potential root causes of the errors."""
    prompt = f"""You are a root cause analyst. Based on the extracted information from the Kafka log, identify potential root causes for the critical errors. Here is the extracted information:\n{state['extracted_info']}\nPlease provide a detailed analysis of potential root causes."""

    response = llm.invoke(prompt)
    return {"root_cause": response.content}


builder = StateGraph(Kafkalogstate)

builder.add_node("log_extraction", log_extraction)
builder.add_node("root_cause_analysis", root_cause_analysis)

builder.add_edge(START, "log_extraction")
builder.add_edge("log_extraction", "root_cause_analysis")
builder.add_edge("log_extraction", "incident_ticket_creation")
builder.add_edge("root_cause_analysis", "solution_agent")
builder.add_edge("solution_agent", "incident_ticket_update")
builder.add_edge("incident_ticket_update", END)

app = builder.compile()

output = app.invoke({"raw_log": "2024-06-01 12:00:00 ERROR [Producer clientId=producer-1] Failed to send message to topic 'test-topic' partition 0 due to timeout."})   

print(output["extracted_info"])
print(output["root_cause"])




