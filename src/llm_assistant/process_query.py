import logging
from langchain_core.messages import HumanMessage

from src.llm_assistant.graph import app

logger = logging.getLogger(__name__)

def process_query(stream_input, thread_config=None):

    for step in app.stream(
        input={"messages": [HumanMessage(stream_input)]}, 
        stream_mode="values"
    ):
        result = step["messages"][-1]
        logger.info(f'STEP:\n{result.pretty_repr()}')
    
    return {"response": result.content}