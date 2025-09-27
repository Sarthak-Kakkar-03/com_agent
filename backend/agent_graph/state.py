
# state.py
from typing import TypedDict, Literal, List, Dict, Any

NextStep = Literal["MAIL", "INFO", "MESSAGE", "supervisor"]

class OverallState(TypedDict, total=False):
    # UI-facing transcript (bounded by pruning)
    visible_messages: List[str]
    # short rolling summary of the conversation
    summary: str # Deprecated, too much overhead
    # routing / info
    latest_info: str
    next: NextStep
    # actor metadata
    name: str
    email: str
    # side-effect/audit log (bounded)
    events: List[Dict[str, Any]]
    # mail tool execution (compact; no LC objects)
    pending_tools: List[Dict[str, Any]]
    last_mail_ai_text: str
    # optional scratch space
    supervisor_instruction: str
    intermediate_note: str

def get_visible_transcript(visible_messages: List[str]) -> str:
    """Join the visible transcript block."""
    return "\n".join(visible_messages or [])
