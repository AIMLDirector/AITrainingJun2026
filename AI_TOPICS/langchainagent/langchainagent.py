from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7
import os
from dotenv import load_dotenv
load_dotenv()

config = {"configurable": {"thread_id": str(uuid7())}}

agent = create_agent(model="ollama:qwen3-vl:8b",
                    system_prompt="you are an helpful AI assisstant ",
                    checkpointer=InMemorySaver()
                    )


while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nBot: Goodbye!")
        break
    else:
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]},config=config)
        print(response["messages"][-1].content)
