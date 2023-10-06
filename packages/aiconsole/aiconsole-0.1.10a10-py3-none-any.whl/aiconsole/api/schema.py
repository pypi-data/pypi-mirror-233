from typing import List

from pydantic import BaseModel

from aiconsole.aic_types import StaticManual, ConversationHeadline, GPTMessageExtended
from aiconsole.gpt.gpt_types import GPTMessage


class BaseGptHTTPRequest(BaseModel):
    conversation_id: str
    messages: List[GPTMessage]


class ExecuteHTTPRequest(BaseGptHTTPRequest):
    agent: str
    relevant_manuals: List[StaticManual]


class AnalyseHTTPRequest(BaseGptHTTPRequest):
    pass


class CommandHistoryPostRequest(BaseModel):
    command: str


class ConversationHistoryHTTPRequest(BaseModel):
    conversation_id: str
    messages: List[GPTMessageExtended]


class ConversationHeadlinesHTTPRequest(BaseModel):
    headlines: List[ConversationHeadline]
