import operator
from typing import Annotated, TypedDict, List, Any, Dict
from langchain_core.messages import AnyMessage, BaseMessage


class OverallState(TypedDict):
    '''
    Overall state object of the communication agent
    '''
    messages: List[BaseMessage]  # The messages holding the memory
    name: str  # name of the employer
    email: str  # email of the employer
    visible_messages: List[str]  # The messages that have been displayed
    latest_info: str  # Info holder for agent internal commands
    next: str  # next agent to target
