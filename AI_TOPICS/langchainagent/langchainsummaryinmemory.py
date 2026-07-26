from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

load_dotenv()

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20)
        )
    ],
    checkpointer=InMemorySaver()
)

config = RunnableConfig(
    configurable={
        "thread_id": "demo"
    }
)

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