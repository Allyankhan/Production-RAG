from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.graph.nodes import (
    retrieve_documents,
    generate_answer,
)

builder = StateGraph(GraphState)

builder.add_node("retrieve", retrieve_documents)
builder.add_node("generate", generate_answer)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()