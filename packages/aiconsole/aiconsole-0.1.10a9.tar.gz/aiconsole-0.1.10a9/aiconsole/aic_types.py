from typing import AsyncGenerator, Callable, List

from pydantic import BaseModel

from aiconsole.gpt.gpt_types import GPTMessage
from aiconsole.gpt.consts import GPTMode


class AgentBase(BaseModel):
    id: str
    name: str
    usage: str
    system: str


class Agent(AgentBase):
    execution_mode: Callable[['ExecutionTaskContext'], AsyncGenerator[str, None]]
    gpt_mode: GPTMode


class BaseTaskContext(BaseModel):
    messages: List[GPTMessage]
    agent: Agent
    mode: GPTMode


class ContentTaskContext(BaseTaskContext):
    relevant_manuals: List["Manual"]


class ExecutionTaskContext(BaseTaskContext):
    relevant_manuals: List["StaticManual"]


class BaseManual(BaseModel):
    id: str
    usage: str


class Manual(BaseManual):
    content: Callable[['ContentTaskContext'], str]


class StaticManual(BaseManual):
    content: str


class GPTMessageExtended(GPTMessage):
    id: str
    agent: AgentBase
    manuals: List[StaticManual]
    timestamp: str


class ConversationHeadline(BaseModel):
    conversation_id: str
    first_message: str
