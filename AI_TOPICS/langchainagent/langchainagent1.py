import os
import requests

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7

from langchain.agents import AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime
from langgraph.graph.message import RemoveMessage

load_dotenv()



SN_INSTANCE = os.getenv("SERVICENOW_INSTANCE")
SN_USER = os.getenv("SERVICENOW_USER")
SN_PASSWORD = os.getenv("SERVICENOW_PASSWORD")


@tool
def create_incident(
    short_description: str,
    urgency: str = "3",
    impact: str = "3",
) -> str:
    """
    Create a ServiceNow Incident.
    """

    url = f"{SN_INSTANCE}/api/now/table/incident"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "short_description": short_description,
        "urgency": urgency,
        "impact": impact,
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            auth=(SN_USER, SN_PASSWORD),
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()["result"]

        number = result["number"]
        sys_id = result["sys_id"]

        return (
            f"Incident created successfully.\n"
            f"Incident Number : {number}\n"
            f"Sys ID          : {sys_id}"
        )

    except Exception as e:
        return f"Unable to create incident.\n{e}"




@after_model
def trim_messages(
    state: AgentState,
    runtime: Runtime,
):

    messages = state["messages"]

    if len(messages) > 8:

        return {
            "messages": [
                RemoveMessage(id=m.id)
                for m in messages[:-8]
            ]
        }

    return None



agent = create_agent(
    model="gpt-4.1-mini",
    tools=[create_incident],
    middleware=[trim_messages],
    system_prompt="""
You are an AI ServiceNow Assistant.

When the user wants to create an incident,
collect

- short_description
- urgency
- impact

and call the ServiceNow tool.

Always respond politely.
""",
    checkpointer=InMemorySaver(),
)




config = {
    "configurable": {
        "thread_id": str(uuid7())
    }
}


print("=" * 60)
print("      ServiceNow AI Agent")
print("=" * 60)

while True:

    question = input("\nYou : ")

    if question.lower() in [
        "exit",
        "quit",
        "bye",
    ]:
        print("\nAssistant : Goodbye.")
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        },
        config=config,
    )

    print("\nAssistant :")
    print(response["messages"][-1].content)
