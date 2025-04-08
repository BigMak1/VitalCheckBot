from typing import Literal

from src.llm_assistant.models import OpenAIChatModel
from src.llm_assistant.prompts import router_prompt, rag_prompt, other_prompt
from src.llm_assistant.graph.state import RouterState, Router
from src.vector_store import vector_store_analysis, vector_store_procedures


router_model = router_prompt | OpenAIChatModel(temperature=0).create_model().with_structured_output(Router)
rag_model = rag_prompt | OpenAIChatModel(temperature=0).create_model()
other_model = other_prompt | OpenAIChatModel().create_model()


def router_node(state: RouterState):
    """Router node to route to next worker."""
    messages = state["messages"]
    route = router_model.invoke({"messages": messages})
    return {"next": route["next"]}


def route_after_prediction(
    state: RouterState,
) -> Literal["rag_acts_analysis_node", "rag_rejection_procedures_node", "other_node"]:
    if state["next"] == "acts_analysis":
        return "rag_acts_analysis_node"
    elif state["next"] == "rejection_procedures":
        return "rag_rejection_procedures_node"
    else:
        return "other_node"
    

def rag_acts_analysis_node(state: RouterState) -> str:
    """Acts analysis node."""
    user_question = state["messages"][-1].content
    relevant_docs = vector_store_analysis.similarity_search(user_question, k=3)
    context_list = [f'Ситуация: {relevant_docs[i].metadata["situation"]}\nОценка критичности, рекомендации: {relevant_docs[i].metadata["assessment"]}' for i in range(len(relevant_docs))]
    context_list = list(set(context_list))  # Remove duplicates
    context = "\n\n".join(context_list)
    
    response = rag_model.invoke({"context": context, "question": user_question})
    return {"messages": [response]}


def rag_rejection_procedures_node(state: RouterState) -> str:
    """Rejection procedures node."""
    user_question = state["messages"][-1].content
    relevant_docs = vector_store_procedures.similarity_search(user_question, k=3)
    context_list = [f'Ситуация: {relevant_docs[i].metadata["situation"]}\nНеобходимые мероприятия юридического подразделения:  {relevant_docs[i].metadata["action"]}' for i in range(len(relevant_docs))]
    context_list = list(set(context_list))  # Remove duplicates
    context = "\n\n".join(context_list)
    
    response = rag_model.invoke({"context": context, "question": user_question})
    return {"messages": [response]}


def other_node(state: RouterState):
    """Other node."""
    user_question = state["messages"][-1].content
    response = other_model.invoke({"user_question": user_question})
    return {"messages": [response]}
