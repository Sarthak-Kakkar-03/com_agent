
# node.py
import logging
from typing import Literal, List, Dict, Any

from .info_agent import info_chain
from .supervisor import supervisor_chain
from .mail_agent import mail_chain, send_direct_mail, send_mail
from .message import message_chain
from .state import OverallState, get_visible_transcript
from .information import PROFILE_OWNER_EMAIL

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

logger = logging.getLogger(__name__)

def _append_ai(state: OverallState, text: str) -> None:
    state.setdefault("visible_messages", []).append("Bot_Message: " + text)

def _last_user_visible(state: OverallState) -> str:
    for msg in reversed(state.get("visible_messages", [])):
        if not msg.startswith("Bot_Message:"):
            return msg
    return ""

def _build_lc_messages(visible_messages: List[str], k: int = 6):
    msgs = []
    for t in visible_messages[-k:]:
        if t.startswith("Bot_Message:"):
            msgs.append(AIMessage(content=t[len("Bot_Message:"):].strip()))
        else:
            msgs.append(HumanMessage(content=t))
    return msgs

def _prune_state(state: OverallState, keep_visible: int = 12, keep_events: int = 50) -> None:
    vm = state.get("visible_messages", [])
    if len(vm) > keep_visible:
        state["visible_messages"] = vm[-keep_visible:]
    ev = state.get("events", [])
    if len(ev) > keep_events:
        state["events"] = ev[-keep_events:]
    # drop bulky intermediates
    for key in ("pending_tools", "last_mail_ai_text", "supervisor_instruction", "intermediate_note"):
        # keep pending_tools only until executed
        if key != "pending_tools":
            state.pop(key, None)


def supervisor_node(state: OverallState) -> OverallState:
    """The node function for the supervisor agent."""
    response = supervisor_chain.invoke({"visible_messages": state.get("visible_messages", [])})
    # visible route explanation
    state.setdefault("visible_messages", []).append("Bot_Message: " + response.display_message)
    # store plain instruction (no LC objects)
    state["supervisor_instruction"] = response.supervisor_message
    state["next"] = response.next
    state["latest_info"] = state.get("latest_info") or "No info collected"
    return state

def supervisor_choice(state: OverallState) -> Literal["mail", "message", "info"]:
    nxt = state.get("next")
    if nxt == "MAIL":
        return "mail"
    if nxt == "INFO":
        return "info"
    return "message"

def info_node(state: OverallState) -> OverallState:
    """Retrieve information about the profile owner to inform the agent."""
    query = _last_user_visible(state)
    response = info_chain.invoke({"query": query})
    state["latest_info"] = response.info_message
    state["intermediate_note"] = response.message  # optional scratch note for message node
    return state

def mail_node(state: OverallState) -> OverallState:
    """Generate mail content; capture tool-calls compactly if produced."""
    supervisor_instruction = state.get("supervisor_instruction", "")
    resp = mail_chain.invoke(
        {
            "visible_messages": state.get("visible_messages", []),
            "employer_name": state["name"],
            "employer_email": state["email"],
            "supervisor_instruction": supervisor_instruction,
        }
    )
    tool_calls = getattr(resp, "tool_calls", None) or []
    state["pending_tools"] = [
        {"id": tc.get("id"), "name": tc.get("name"), "args": tc.get("args")}
        for tc in tool_calls
    ]
    state["last_mail_ai_text"] = getattr(resp, "content", "")
    return state

def choose_tools_or_messages(state: OverallState) -> Literal["message", "mail_tool"]:
    pending = state.get("pending_tools") or []
    if pending:
        # Notify the profile owner via a direct mail that a mail was generated
        transcript = get_visible_transcript(state.get("visible_messages", []))
        notify = (
            f"A mail was generated for mail id: {state['email']} and name: {state['name']}.\n\n"
            f"Conversation so far:\n{transcript}"
        )
        _ = send_direct_mail(notify, PROFILE_OWNER_EMAIL)
        return "mail_tool"
    # log event; continue to message
    state.setdefault("events", []).append({"type": "mail", "status": "no_tool_call"})
    return "message"

def mail_tool_node(state: OverallState) -> OverallState:
    """Execute pending send_mail tool-calls and log compact results."""
    for tc in state.get("pending_tools", []) or []:
        try:
            observation = send_mail.invoke(tc.get("args", {}))
            state.setdefault("events", []).append(
                {"type": "tool_result", "tool": tc.get("name"), "result": str(observation), "id": tc.get("id")}
            )
        except Exception as e:
            state.setdefault("events", []).append(
                {"type": "tool_error", "tool": tc.get("name"), "error": str(e), "id": tc.get("id")}
            )
    # clear after execution
    state["pending_tools"] = []
    return state

def message_node(state: OverallState) -> OverallState:
    """Formats and generates the final message back to the employer."""
    lc_msgs = _build_lc_messages(state.get("visible_messages", []), k=6)

    response = message_chain.invoke(
        {
            "visible_conversation": state.get("visible_messages", []),
            "invisible_conversation": [m.content for m in lc_msgs],
            "info": state.get("latest_info", ""),
            "employer_name": state["name"],
        }
    )

    _append_ai(state, response.chat_response)
    _prune_state(state)
    return state
