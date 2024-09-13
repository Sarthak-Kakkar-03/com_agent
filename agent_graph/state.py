import operator
from typing import Annotated, TypedDict, List, Any, Dict
from langchain_core.messages import AnyMessage, BaseMessage

class OverallState(TypedDict):
    '''
    Overall state of the communication agent
    '''
    messages: List[BaseMessage]
    name: str
    email: str
    display_messages: List[str]
    counter: int
