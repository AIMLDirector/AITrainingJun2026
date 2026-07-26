from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import (AgentMiddleware,SummarizationMiddleware)
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

load_dotenv()

class PromptInjectionMiddleware(AgentMiddleware):
    def before_model(
        self,
        state,
        runtime
    ):
        latest_message = (
            state["messages"][-1]
            .content
            .lower()
        )
        blocked_patterns = [
            "ignore previous instructions",
            "ignore all instructions",
            "forget previous instructions",
            "override instructions",
            "show system prompt",
            "reveal system prompt",
            "display system prompt",
            "show hidden instructions",
            "developer instructions",
            "internal instructions",
            "hidden prompt",
            "jailbreak",
            "bypass guardrails",
            "disable safety",
            "act as unrestricted",
            "act as root",
            "repeat your instructions",
            "print your instructions",
            "show configuration",
            "show chain of thought"
        ]

        for pattern in blocked_patterns:
            if pattern in latest_message:
                raise ValueError(
                    f"Prompt Injection Detected: {pattern}"
                )
        return None


checkpointer = InMemorySaver()

agent = create_agent(
    model="gpt-5.4",
    tools=[],
    middleware=[
        PromptInjectionMiddleware(),
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20)
        )
    ],
    checkpointer=checkpointer,
)
config = RunnableConfig(
    configurable={
        "thread_id": "chat_session_001"
    }
)

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye" ]:
            print("\nBot: Goodbye!")
            break
        response = agent.invoke(
            {
                "messages": [{"role": "user", "content": user_input}],
                "user_id": "user_001"
            },
            config=config
        )
        print("\nBot:", response["messages"][-1].content)
        print()
    except Exception as e:
        print(f"\nBlocked: {str(e)}\n")