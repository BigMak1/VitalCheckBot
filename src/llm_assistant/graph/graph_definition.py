from typing import Literal

from langgraph.graph import StateGraph, START, END

from src.llm_assistant.graph.state import RouterState
from src.llm_assistant.graph.nodes import (
    router_node,
    route_after_prediction,
    rag_acts_analysis_node,
    rag_rejection_procedures_node,
    other_node,
)

graph = StateGraph(RouterState)

# DEFINE NODES:
graph.add_node("router_node", router_node)
graph.add_node("rag_acts_analysis_node", rag_acts_analysis_node)
graph.add_node("rag_rejection_procedures_node", rag_rejection_procedures_node)
graph.add_node("other_node", other_node)

# DEFINE EDGES
graph.add_edge(START, "router_node")
graph.add_conditional_edges("router_node", route_after_prediction)
graph.add_edge("rag_acts_analysis_node", END)
graph.add_edge("rag_rejection_procedures_node", END)
graph.add_edge("other_node", END)

app = graph.compile()