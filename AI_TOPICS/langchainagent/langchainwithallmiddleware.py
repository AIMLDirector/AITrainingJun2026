from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import (
    PIIMiddleware,
    SummarizationMiddleware,
    AgentMiddleware
)

from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.runnables import RunnableConfig

load_dotenv()


class DebugMiddleware(AgentMiddleware):

    def before_model(
        self,
        state,
        runtime
    ):

        print("\n----- Message Sent To Model -----")
        print(state["messages"][-1].content)
        print("---------------------------------\n")

        return None


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    max_tokens=600,
    max_retries=2
)


checkpointer = InMemorySaver()


agent = create_agent(
    model=llm,
    system_prompt="""
    You are a helpful assistant of Data Engineering team.
    Provide clear and concise answers.
    """,
    tools=[],
    middleware=[

        PIIMiddleware(
            "email",
            strategy="mask",
            apply_to_input=True
        ),


        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True
        ),

        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20)
        ),

        DebugMiddleware()
    ],
    checkpointer=checkpointer
)


config = RunnableConfig(
    configurable={
        "thread_id": "chat_session_001"
    }
)


while True:

    user_input = input("You: ")

    if user_input.lower() in [
        "exit",
        "quit",
        "bye"
    ]:

        print("\nBot: Goodbye!")
        break

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                "user_id": "user_001"
            },
            config=config
        )

        print(
            "\nBot:",
            response["messages"][-1].content
        )
        print()

    except Exception as e:

        print(
            f"\nError: {str(e)}\n"
        )