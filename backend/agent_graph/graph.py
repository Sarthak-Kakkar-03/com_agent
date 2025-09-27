
# graph.py
import logging

from langgraph.graph import StateGraph

from .node import (
    supervisor_node,
    supervisor_choice,
    info_node,
    mail_node,
    message_node,
    mail_tool_node,
    choose_tools_or_messages,
)
from .state import OverallState, get_visible_transcript

logger = logging.getLogger(__name__)

def build_graph():
    workflow = StateGraph(OverallState)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("info", info_node)
    workflow.add_node("mail", mail_node)
    workflow.add_node("mail_tool", mail_tool_node)
    workflow.add_node("message", message_node)

    workflow.set_entry_point("supervisor")
    workflow.add_conditional_edges("supervisor", supervisor_choice, {
        "info": "info",
        "mail": "mail",
        "message": "message",
    })
    # mail path
    workflow.add_conditional_edges("mail", choose_tools_or_messages, {
        "mail_tool": "mail_tool",
        "message": "message",
    })
    workflow.add_edge("mail_tool", "message")
    # info path goes straight to message
    workflow.add_edge("info", "message")

    return workflow.compile()


