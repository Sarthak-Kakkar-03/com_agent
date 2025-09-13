# node.py
import logging
from typing import Literal, List

from info_agent import info_chain
from supervisor import supervisor_chain
from mail_agent import mail_chain, send_direct_mail, send_mail
from message import message_chain
from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage
from state import OverallState, get_visible_transcript

logger = logging.getLogger(__name__)


def _contents(messages: List[BaseMessage]) -> List[str]:
    """Extract .content strings from messages, skipping items without content."""
    out: List[str] = []
    for m in messages:
        try:
            out.append(getattr(m, "content", ""))
        except Exception:
            out.append("")
    return out


def supervisor_node(state: OverallState) -> OverallState:
    """
    The node function for the supervisor agent.
    """
    messages_as_string = _contents(state["messages"])
    response = supervisor_chain.invoke(
        {"messages_as_string": messages_as_string, "visible_messages": state["visible_messages"]}
    )
    # Show a concise display message to employer
    state["visible_messages"].append("Bot_Message: " + response.display_message)
    # Add internal instruction for next agent
    supervisor_instruction = HumanMessage(content=response.supervisor_message)
    state["messages"].append(supervisor_instruction)
    state["next"] = response.next
    state["latest_info"] = state.get("latest_info") or "No info collected"
    return state


def supervisor_choice(state: OverallState) -> Literal["mail", "message", "info"]:
    """
    Decider function for the next node.
    """
    nxt = state.get("next")
    if nxt == "MAIL":
        return "mail"
    if nxt == "INFO":
        return "info"
    return "message"


def info_node(state: OverallState) -> OverallState:
    """
    The node that retrieves information about Sarthak to inform the agent.
    """
    query = state["messages"][-1].content
    response = info_chain.invoke({"query": query})
    # Add an internal communication message for the downstream message node
    communication_message = HumanMessage(content=response.message)
    state["messages"].append(communication_message)
    state["latest_info"] = response.info_message
    return state


def mail_node(state: OverallState) -> OverallState:
    """
    The function node to generate the mail content (will result in a tool call if LLM decides).
    """
    supervisor_instruction = state["messages"][-1].content
    response = mail_chain.invoke(
        {
            "visible_messages": state["visible_messages"],
            "employer_name": state["name"],
            "employer_email": state["email"],
            "supervisor_instruction": supervisor_instruction,
        }
    )
    # The response here is an AIMessage that may include tool_calls
    state["messages"].append(response)
    return state


def choose_tools_or_messages(state: OverallState) -> Literal["message", "mail_tool"]:
    """
    Decide whether to execute a tool call from the last AI message or move on to the message node.
    """
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", None)

    if tool_calls:
        # Notify Sarthak via a direct mail that a mail was generated
        transcript = get_visible_transcript(state["visible_messages"])
        notify = (
            f"A mail was generated for mail id: {state['email']} and name: {state['name']}.\n\n"
            f"Conversation so far:\n{transcript}"
        )
        _ = send_direct_mail(notify, "sarthakkakkar2021@gmail.com")
        return "mail_tool"

    # No tool call produced; let the employer know something went wrong and continue as message
    state["messages"].append(HumanMessage(content="Mail node failed to call the mail tool"))
    return "message"


def mail_tool_node(state: OverallState) -> OverallState:
    """
    Tool node for the mail function, invokes the send_mail tool calls produced by the LLM.
    """
    last = state["messages"][-1]
    for tool_call in getattr(last, "tool_calls", []) or []:
        # Map tool name to function (only one tool here)
        observation = send_mail.invoke(tool_call["args"])
        tool_result = ToolMessage(content=observation, tool_call_id=tool_call["id"])
        state["messages"].append(tool_result)
    return state


def message_node(state: OverallState) -> OverallState:
    """
    Formats and generates the final message back to the employer.
    """
    invisible_conversation = _contents(state["messages"])
    visible_conversation = state["visible_messages"]

    response = message_chain.invoke(
        {
            "visible_conversation": visible_conversation,
            "invisible_conversation": invisible_conversation,
            "info": state["latest_info"],
            "employer_name": state["name"],
        }
    )

    state["visible_messages"].append("Bot_Message: " + response.chat_response)
    state["messages"].append(
        HumanMessage(content="Responded to the employer with the message: " + response.chat_response)
    )
    return state
