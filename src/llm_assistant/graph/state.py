from typing import Literal, TypedDict
from langgraph.graph import MessagesState


class RouterState(MessagesState):
    next: Literal["acts_analysis", "rejection_procedures", "other"]


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to other."""
    next: Literal["acts_analysis", "rejection_procedures", "other"]