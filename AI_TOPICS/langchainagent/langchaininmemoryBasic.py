from typing import Annotated
import operator
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver


class CustomAgentState(AgentState):
    user_id: str

memory = InMemorySaver()


agent = create_agent(
    model="gpt-4.1-mini",

    tools=[],

    state_schema=CustomAgentState,

    checkpointer=memory,

    system_prompt="""
You are a helpful AI assistant.

Rules:
- Remember previous conversation
- Answer naturally
- Maintain context
- Be conversational
"""
)



config = {
    "configurable": {
        "thread_id": "chat_session_001"
    }
}

print("\nAI Chatbot Started")
print("Type 'exit' to stop\n")


while True:

    user_input = input("You: ")

    # Exit Condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nBot: Goodbye!")
        break

    # Invoke Agent
    response = agent.invoke(
        {
            "messages": [{"role": "user","content": user_input}],
            "user_id": "user_001"
        },
        config=config
    )

    # Print Response
    print("\nBot:", response["messages"][-1].content)
    print()