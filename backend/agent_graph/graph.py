# graph.py
import logging

from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

from node import (
    supervisor_node,
    supervisor_choice,
    info_node,
    mail_node,
    message_node,
    mail_tool_node,
    choose_tools_or_messages,
)
from state import OverallState
from configs import set_env

set_env()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Build the workflow
workflow = StateGraph(OverallState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("info", info_node)
workflow.add_node("mail", mail_node)
workflow.add_node("mail_tool", mail_tool_node)
workflow.add_node("message", message_node)

workflow.add_edge("__start__", "supervisor")
workflow.add_conditional_edges("supervisor", supervisor_choice)
workflow.add_conditional_edges("mail", choose_tools_or_messages)
workflow.add_edge("info", "message")
workflow.add_edge("mail_tool", "message")
workflow.add_edge("message", "__end__")

if __name__ == "__main__":
    try:
        com_agent = workflow.compile()
        result = com_agent.invoke(
            {
                "messages": [HumanMessage(content="tell me about sarthak")],
                "name": "Ayan",
                "email": "test@gmail.com",
                "visible_messages": ["tell sarthak to contact me"],
                "latest_info": "",
                "next": "supervisor",
            }
        )
        print(result)
    except Exception as e:
        logger.exception("Agent run failed")
