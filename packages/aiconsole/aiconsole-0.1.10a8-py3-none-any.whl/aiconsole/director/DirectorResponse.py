from typing import List
from typing_extensions import TypedDict

class AgentDict(TypedDict):
    id: str
    name: str
    usage: str
    system: str
    execution_mode: str

class ManualDict(TypedDict):
    id: str
    usage: str
    content: str

class DirectorResponse(TypedDict):
    next_step: str
    agent: AgentDict | None
    manuals: List[ManualDict]
