from langchain.agents import create_agent
import requests
import os
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()


SERVICENOW_INSTANCE = os.getenv("SERVICENOW_INSTANCE")  
SERVICENOW_USER = os.getenv("SERVICENOW_USER")
SERVICENOW_PASSWORD = os.getenv("SERVICENOW_PASSWORD")

@tool
def create_servicenow_ticket(short_description: str, description: str, urgency: int = 3) -> str:
    """Create a new incident ticket in ServiceNow.
    
    Args:
        short_description: A brief summary of the issue.
        description: Detailed explanation of the issue.
        urgency: Urgency level (1=High, 2=Medium, 3=Low).
    """
    url = f"https://{SERVICENOW_INSTANCE}/api/now/table/incident"
    payload = {
        "short_description": short_description,
        "description": description,
        "urgency": str(urgency)
    }
    
    response = requests.post(url, json=payload, auth=auth, headers=headers)
    if response.status_code == 201:
        data = response.json().get("result", {})
        return f"Successfully created ticket {data.get('number')} with Sys ID {data.get('sys_id')}."
    return f"Failed to create ticket: {response.text}"

@tool
def update_servicenow_ticket(sys_id: str, work_notes: str) -> str:
    """Update an existing incident ticket in ServiceNow with new work notes.
    
    Args:
        sys_id: The unique system identifier (sys_id) of the incident ticket.
        work_notes: The updated notes or comments to append to the ticket.
    """
    url = f"https://{SERVICENOW_INSTANCE}/api/now/table/incident/{sys_id}"
    payload = {"work_notes": work_notes}
    
    response = requests.patch(url, json=payload, auth=auth, headers=headers)
    if response.status_code == 200:
        data = response.json().get("result", {})
        return f"Successfully updated ticket {data.get('number')}."
    return f"Failed to update ticket: {response.text}"

@tool
def close_servicenow_ticket(sys_id: str, close_notes: str) -> str:
    """Close an existing incident ticket in ServiceNow.
    
    Args:
        sys_id: The unique system identifier (sys_id) of the incident ticket.
        close_notes: Reason or resolution details for closing the ticket.
    """
    url = f"https://{SERVICENOW_INSTANCE}/api/now/table/incident/{sys_id}"
    # State '7' typically represents Closed/Resolved in baseline ServiceNow configurations
    payload = {
        "state": "7",
        "close_notes": close_notes
    }
    
    response = requests.patch(url, json=payload, auth=auth, headers=headers)
    if response.status_code == 200:
        data = response.json().get("result", {})
        return f"Successfully closed ticket {data.get('number')}."
    return f"Failed to close ticket: {response.text}"

auth = (SERVICENOW_USER, SERVICENOW_PASSWORD)
headers = {"Content-Type": "application/json", "Accept": "application/json"}
agents = create_agent(model="gpt-4o-mini", 
                        system_prompt="You are helpful AI assistant in Developer side",
                        tools=[create_servicenow_ticket,update_servicenow_ticket, close_servicenow_ticket ], 
                    
                       )

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nBot: Goodbye!")
        break
    else:
        response = agents.invoke({"messages": [{"role": "user", "content": user_input}]})
        print(response["messages"][-1].content)
        
