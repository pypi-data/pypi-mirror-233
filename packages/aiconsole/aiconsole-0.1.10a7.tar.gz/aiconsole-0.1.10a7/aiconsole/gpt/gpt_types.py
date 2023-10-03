import decimal
from typing import Literal, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict

Role = Literal["user", "assistant", "system"]


class GPTMessage(BaseModel):
    role: Role
    content: str


class EnforcedFunctionCall(TypedDict):
    name: str


class GPTFunctionCallInvocation(TypedDict):
    name: str
    arguments: str


class GPTResult(BaseModel):
    content: str
    function_call: Optional[GPTFunctionCallInvocation]
    cost: decimal.Decimal
