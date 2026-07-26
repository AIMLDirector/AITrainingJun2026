from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents.middleware import PIIMiddleware
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


# Initialize the LangChain OpenAI chat model
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    max_tokens=600,
    max_retries=2
)

# PII_filter = PIIMiddleware(
#     pii_types=["email","credit_card"],
#     strategy="mask"
# )
config = {
    "configurable": {
        "thread_id": "chat_session_001"
    }
}

agent = create_agent(
            model=llm,
            system_prompt="You are a helpful assistant of Data engineering team and SME . provide clear and concise answers to user queries related to data engineering topics.",
            tools=[],
            middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
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
