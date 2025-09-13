# state.py
from typing import TypedDict, List, Literal
from langchain_core.messages import BaseMessage


class OverallState(TypedDict):
    """
    Overall state object of the communication agent.
    Keys are mutated by graph nodes, so we keep a TypedDict
    (LangGraph plays nicer with dict-like state than with pydantic models).
    """
    messages: List[BaseMessage]            # Conversation memory (internal + tool messages)
    name: str                              # Employer/person name
    email: str                             # Employer/person email
    visible_messages: List[str]            # Messages shown to the employer
    latest_info: str                       # Info fetched by info agent
    next: Literal["MAIL", "INFO", "MESSAGE", "supervisor"]  # Next agent decision


def get_visible_transcript(visible_messages: List[str]) -> str:
    """Utility: Join visible messages into a single transcript block."""
    return "\n".join(visible_messages or [])
