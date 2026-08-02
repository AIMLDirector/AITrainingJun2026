
from langgraph.graph import StateGraph, END
from state import IncidentState
from agents.nodes import java_node, infra_node, network_node, recommendation_node

builder=StateGraph(IncidentState)
builder.add_node("java",java_node)
builder.add_node("infra",infra_node)
builder.add_node("network",network_node)
builder.add_node("recommendation",recommendation_node)

builder.set_entry_point("java")
builder.add_edge("java","infra")
builder.add_edge("infra","network")
builder.add_edge("network","recommendation")
builder.add_edge("recommendation",END)

graph=builder.compile()
