from datetime import datetime
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain.agents.middleware import before_agent, before_model, after_model, after_agent, wrap_tool_call
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72°F and sunny in {city}."


@tool
def search_knowledge(query: str) -> str:
    """Search internal company knowledge base."""
    return f"Internal knowledge for '{query}': Hybrid RAG (Dense + BM25) is the recommended approach in 2026."


@tool
def calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


tools = [get_weather, search_knowledge, calculate]


def _get_thread_id(runtime) -> str:
    """Safely extract thread_id from different runtime shapes."""
    if runtime is None:
        return "unknown"

    # Case 1: runtime.config exists
    if hasattr(runtime, "config") and runtime.config:
        return runtime.config.get("configurable", {}).get("thread_id", "unknown")

    # Case 2: runtime itself is a dict-like config
    if isinstance(runtime, dict):
        return runtime.get("configurable", {}).get("thread_id", "unknown")

    # Case 3: runtime has .configurable
    if hasattr(runtime, "configurable"):
        return getattr(runtime, "configurable", {}).get("thread_id", "unknown")

    return "unknown"


@before_agent
def log_before_agent(state, runtime):
    thread_id = _get_thread_id(runtime)
    print(f"\n[before_agent] Starting agent | thread_id={thread_id}")
    return None


@before_model
def log_before_model(state, runtime):
    num_messages = len(state.get("messages", []))
    print(f"[before_model] Calling LLM | messages in state: {num_messages}")
    return None


@after_model
def log_after_model(state, runtime):
    messages = state.get("messages", [])
    if messages:
        last = messages[-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            tool_names = [tc["name"] for tc in last.tool_calls]
            print(f"[after_model] Model requested tools -> {tool_names}")
        else:
            print("[after_model] Model responded with final answer")
    return None


@after_agent
def log_after_agent(state, runtime):
    print(f"[after_agent] Agent finished at {datetime.now().strftime('%H:%M:%S')}")
    return None


@wrap_tool_call
def log_tool_call(request, handler):
    tool_name = request.tool_call["name"]
    tool_args = request.tool_call.get("args", {})
    print(f"  [wrap_tool_call] Executing -> {tool_name}({tool_args})")

    try:
        result = handler(request)
        print(f"  Tool '{tool_name}' succeeded")
        return result
    except Exception as e:
        print(f"  Tool '{tool_name}' failed: {e}")
        raise


checkpointer = InMemorySaver()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=tools,
    middleware=[
        log_before_agent,
        log_before_model,
        log_after_model,
        log_after_agent,
        log_tool_call,
    ],
    checkpointer=checkpointer,
    system_prompt=(
        "You are a helpful and precise assistant. "
        "Use tools when needed. Keep answers concise and clear."
    ),
)


def chat(user_input: str, thread_id: str = "user-001"):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print(f"\n{'='*60}")
    print(f"User: {user_input}")
    print("=" * 60)

    result = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config,
    )

    final_message = result["messages"][-1]
    print(f"\nAgent: {final_message.content}")
    return final_message.content


if __name__ == "__main__":
    chat("What's the weather in Tokyo?")
    chat("What is that city known for?")
    chat("Calculate 15 * 8 + 20")
    chat("Search knowledge about hybrid RAG systems")