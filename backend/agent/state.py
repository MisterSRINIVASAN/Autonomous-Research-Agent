import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """The state of the agent graph."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
