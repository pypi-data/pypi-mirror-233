import asyncio
import json
from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from openai_function_call import OpenAISchema
from pydantic import Field

from aiconsole.aic_types import SYSTEM_IDENTITY, ContentTaskContext
from aiconsole.api.schema import AnalyseHTTPRequest
from aiconsole.gpt.gpt_executor import GPTExecutor
from aiconsole.gpt.gpt_types import EnforcedFunctionCall
from aiconsole.gpt.request import GPTRequest
from aiconsole.manuals import manuals
from aiconsole.agents import agents
from aiconsole.utils.get_system_content import get_system_content

MIN_TOKENS = 250
PREFERRED_TOKENS = 500

router = APIRouter()

@router.post("/analyse")
async def analyse(request: AnalyseHTTPRequest) -> JSONResponse:
    messages = request.messages
    mode = request.mode

    available_agents = agents.all_agents()
    available_manuals = manuals.all_manuals()

    system_content = get_system_content(
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
        if (chunk.get("error", "")):
            raise ValueError(f"Error in GPT: {chunk.get('error', '')}")

        delta = chunk["choices"][0]["delta"]

        if isinstance(delta, str):
            text_chunk = delta
        elif isinstance(delta, dict):
            text_chunk = delta.get("content", "") or delta.get("function_call", {"arguments": ""}).get("arguments", "") or ""
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

    matching_agents = [
        c for c in available_agents if arguments["agent_id"] == c.id
    ]

    try:
        picked_agent = matching_agents[0]
    except IndexError:
        raise ValueError(f"Could not find agent in the text: {full_result}")
    if picked_agent is None:
        raise Exception("No agent picked")

    relevant_manuals = [k for k in available_manuals if k.id in raw_arguments]

    task_context = ContentTaskContext(
        messages=request.messages,
        agent=picked_agent,
        relevant_manuals=relevant_manuals,
        mode=request.mode,
    )

    analysis = {
        "agent": {
            "id": picked_agent.id,
            "name": picked_agent.name,
            "usage": picked_agent.usage,
            "content": picked_agent.system,
            "execution_mode": picked_agent.execution_mode.__name__,  # TODO: Probably we should keep to the original name
        }
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
        "available_tokens": gpt_request.model,
    }

    print(analysis)

    return JSONResponse(content=analysis)
