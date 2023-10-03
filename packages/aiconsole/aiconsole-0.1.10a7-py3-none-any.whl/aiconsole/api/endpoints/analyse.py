import asyncio
import json
from typing import List
from typing_extensions import TypedDict

from fastapi import APIRouter
from openai_function_call import OpenAISchema
from pydantic import Field

from aiconsole.aic_types import ContentTaskContext
from aiconsole.api.schema import AnalyseHTTPRequest
from aiconsole.gpt.gpt_executor import GPTExecutor
from aiconsole.gpt.gpt_types import EnforcedFunctionCall
from aiconsole.gpt.request import GPTRequest
from aiconsole.manuals import manuals
from aiconsole.agents import agents
from aiconsole.utils.get_analyse_system_content import get_analyse_system_content

MIN_TOKENS = 250
PREFERRED_TOKENS = 500

router = APIRouter()

SYSTEM_IDENTITY = """
You are AI-Console, a director of AI Agents.
You have multiple AI Agents at your disposal, each with their own unique capabilities.
Some of them can run code on this local machine in order to perform any tasks that the user needs.
""".strip()


# TODO these types should be moved to different place
class Agent(TypedDict):
    id: str
    name: str
    usage: str
    system: str
    execution_mode: str


class Manual(TypedDict):
    id: str
    usage: str
    content: str


class AnalyseResponse(TypedDict):
    agent: Agent | None
    manuals: List[Manual]
    used_tokens: int
    available_tokens: int


@router.post("/analyse")
async def analyse(request: AnalyseHTTPRequest) -> AnalyseResponse:
    messages = request.messages
    mode = request.mode

    available_agents = agents.all_agents()
    available_manuals = manuals.all_manuals()

    system_content = get_analyse_system_content(
        system_description=SYSTEM_IDENTITY,
        available_agents=available_agents,
        available_manuals=available_manuals,
    )

    class OutputSchema(OpenAISchema):
        """
        Choose needed manuals and agent for the task.
        """

        needed_manuals_ids: List[str] = Field(
            ...,
            description="Chosen manuals ids needed for the task",
            json_schema_extra={
                "items": {"enum": [k.id for k in available_manuals], "type": "string"}
            },
        )

        agent_id: str = Field(
            ...,
            description="Chosen agent id for the task",
            json_schema_extra={"enum": [s.id for s in available_agents]},
        )

    gpt_request = GPTRequest(
        mode=mode,
        messages=messages,
        functions=[OutputSchema.openai_schema],
        function_call=EnforcedFunctionCall(name="OutputSchema"),
    )
    gpt_request.add_prompt_context(system_content)
    gpt_request.update_max_token(MIN_TOKENS, PREFERRED_TOKENS)

    gpt_executor = GPTExecutor()

    for chunk in gpt_executor.execute(gpt_request):
        if chunk.get("error", ""):
            raise ValueError(f"Error in GPT: {chunk.get('error', '')}")

        delta = chunk["choices"][0]["delta"]

        if isinstance(delta, str):
            text_chunk = delta
        elif isinstance(delta, dict):
            text_chunk = (
                delta.get("content", "")
                or delta.get("function_call", {"arguments": ""}).get("arguments", "")
                or ""
            )
        else:
            raise ValueError(f"Unexpected delta type: {type(delta)}")

        print(text_chunk)
        await asyncio.sleep(0)

    full_result = gpt_executor.full_result
    tokens_used = gpt_executor.tokens_used

    if full_result.function_call is None:
        raise ValueError(f"Could not find function call in the text: {full_result}")

    raw_arguments = full_result.function_call["arguments"]
    arguments = json.loads(raw_arguments, strict=False)

    picked_agent = next(
        (agent for agent in available_agents if agent.id == arguments["agent_id"]), None
    )

    if not picked_agent:
        raise ValueError(f"Could not find agent in the text: {full_result}")

    # TODO raw_arguments might not be accurate to check which manuals are needed
    relevant_manuals = [k for k in available_manuals if k.id in raw_arguments]

    task_context = ContentTaskContext(
        messages=request.messages,
        agent=picked_agent,
        relevant_manuals=relevant_manuals,
        mode=request.mode,
    )

    analysis: AnalyseResponse = {
        "agent": Agent(
            **dict(
                picked_agent.dict()
                | {"execution_mode": picked_agent.execution_mode.__name__}
            ),
        )
        if picked_agent
        else None,
        "manuals": [
            {
                "id": manual.id,
                "usage": manual.usage,
                "content": manual.content(task_context),
            }
            for manual in relevant_manuals
        ],
        "used_tokens": tokens_used,
        "available_tokens": gpt_request.model_data.max_tokens,
    }

    print(analysis)

    return analysis
