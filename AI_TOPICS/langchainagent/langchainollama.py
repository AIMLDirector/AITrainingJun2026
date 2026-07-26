from langchain.agents import create_agent
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen3.5:2b", temperature=0.9)
user_input = input("Enter your message: ")
agent = create_agent(model=model)
response = agent.invoke({"messages": [("user", user_input)]})
print(response["messages"][-1].content)
