from typing import List

from pydantic import BaseModel

from aiconsole.aic_types import StaticManual
from aiconsole.gpt.gpt_types import GPTMessage
from aiconsole.gpt.consts import GPTModeLiteral


class BaseGptHTTPRequest(BaseModel):
    conversation_id: str
    messages: List[GPTMessage]


class ExecuteHTTPRequest(BaseGptHTTPRequest):
    agent: str
    relevant_manuals: List[StaticManual]
    mode: GPTModeLiteral


class AnalyseHTTPRequest(BaseGptHTTPRequest):
    mode: GPTModeLiteral


class CommandHistoryPostRequest(BaseModel):
    command: str
