from typing import AsyncGenerator, Callable, List

from pydantic import BaseModel

from aiconsole.gpt.gpt_types import GPTMessage
from aiconsole.gpt.consts import GPTModeLiteral


class Agent(BaseModel):
    id: str
    name: str
    usage: str
    system: str
    execution_mode: Callable[['ExecutionTaskContext'], AsyncGenerator[str, None]]


class BaseTaskContext(BaseModel):
    messages: List[GPTMessage]
    agent: Agent
    mode: GPTModeLiteral


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
