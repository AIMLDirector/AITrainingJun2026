from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

@tool
def get_current_time(dummy: str = "") -> str:
    """
    Get the current time 
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def get_current_weather(location: str) -> str:
    """
    Get the current weather for a given location
    """
    # This is a placeholder implementation. In a real implementation, you would call a weather API.
    return f"The current weather in {location} is sunny with a temperature of 25°C."

tools = [get_current_time,get_current_weather]

model = ChatOpenAI(model="gpt-5-nano", temperature=0.9)
user_input = input("Enter your message: ")
agent = create_agent(model=model, tools=tools)

response = agent.invoke({"messages": [("user", user_input)]})
print(response["messages"][-1].content)
