import os
from typing import TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.5",
    temperature=0
)


@tool
def get_weather(city: str) -> dict:
    weather_data = {
        "Bangalore": {
            "city": "Bangalore",
            "temperature": 29,
            "condition": "Sunny"
        },
        "Chennai": {
            "city": "Chennai",
            "temperature": 34,
            "condition": "Hot"
        },
        "Mumbai": {
            "city": "Mumbai",
            "temperature": 31,
            "condition": "Cloudy"
        }
    }

    return weather_data.get(
        city,
        {
            "city": city,
            "temperature": 25,
            "condition": "Unknown"
        }
    )


class WeatherResponse(BaseModel):
    city: str
    temperature: float = Field(...)
    condition: str


class AgentState(TypedDict):
    question: str
    city: str
    tool_output: dict
    validated: bool
    answer: str


def extract_city_node(state: AgentState):
    question = state["question"]
    city = question.split()[-1].replace("?", "")
    state["city"] = city
    return state


def tool_node(state: AgentState):
    result = get_weather.invoke({"city": state["city"]})
    state["tool_output"] = result
    return state


def validate_node(state: AgentState):
    try:
        WeatherResponse.model_validate(state["tool_output"])
        state["validated"] = True
    except ValidationError:
        state["validated"] = False
    return state


def router(state: AgentState):
    if state["validated"]:
        return "llm"
    return END


def llm_node(state: AgentState):
    tool_data = WeatherResponse.model_validate(state["tool_output"])

    prompt = f"""
You are an AI assistant.

Use ONLY the weather data below.

Never invent information.

Weather Data:
{tool_data.model_dump_json(indent=2)}

Answer naturally.
"""

    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state


builder = StateGraph(AgentState)

builder.add_node("extract_city", extract_city_node)
builder.add_node("tool", tool_node)
builder.add_node("validate", validate_node)
builder.add_node("llm", llm_node)

builder.set_entry_point("extract_city")

builder.add_edge("extract_city", "tool")
builder.add_edge("tool", "validate")

builder.add_conditional_edges(
    "validate",
    router,
    {
        "llm": "llm",
        END: END,
    },
)

builder.add_edge("llm", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke(
        {
            "question": "What's the weather in Bangalore?"
        }
    )

    print(result["answer"])