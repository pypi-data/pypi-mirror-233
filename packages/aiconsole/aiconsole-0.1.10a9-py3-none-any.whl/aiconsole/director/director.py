import asyncio
import json
import logging
from typing import List
from openai_function_call import OpenAISchema
from pydantic import Field
from aiconsole.agents.agents import agents
from aiconsole.aic_types import Agent, ContentTaskContext
from aiconsole.api.schema import AnalyseHTTPRequest
from aiconsole.director.DirectorResponse import AgentDict, DirectorResponse
from aiconsole.director.rephrase_as_message import rephrase_as_message_for_agent, rephrase_as_message_for_user
from aiconsole.execution_modes.normal import execution_mode_normal
from aiconsole.gpt.consts import GPTMode
from aiconsole.gpt.gpt_executor import GPTExecutor
from aiconsole.gpt.gpt_types import EnforcedFunctionCall
from aiconsole.gpt.request import GPTRequest
from aiconsole.manuals.manuals import manuals
from aiconsole.director.get_director_system_prompt import get_director_system_prompt

DIRECTOR_MIN_TOKENS = 250
DIRECTOR_PREFERRED_TOKENS = 1000

log = logging.getLogger(__name__)


async def director_analyse(request: AnalyseHTTPRequest) -> DirectorResponse:
    messages = request.messages

    available_agents = agents.all_agents()
    available_manuals = manuals.all_manuals()

    # Director can suggest a user only if the last message was not from the user
    if (request.messages and request.messages[-1].role != "user"):
        available_agents = [Agent(id='user', name='User', usage='When a human user needs to respond',
                                  system='', execution_mode=execution_mode_normal, gpt_mode=GPTMode.QUALITY), *available_agents]
    
    system_content = get_director_system_prompt(
        available_agents=available_agents,
        available_manuals=available_manuals,
    )

    class OutputSchema(OpenAISchema):
        """
        Choose needed manuals and agent for the task.
        """

        next_step: str = Field(
            description="A short actionable description of the next single atomic task to move this conversation forward.",
            json_schema_extra={"type": "string"}
        )

        agent_id: str = Field(
            ...,
            description="Chosen agent to perform the next step, can also be the user.",
            json_schema_extra={"enum": [s.id for s in available_agents]},
        )

        needed_manuals_ids: List[str] = Field(
            ...,
            description="Chosen manuals ids needed for the task",
            json_schema_extra={
                "items": {"enum": [k.id for k in available_manuals], "type": "string"}
            },
        )

    gpt_request = GPTRequest(
        mode=GPTMode.FAST,
        messages=messages,
        functions=[OutputSchema.openai_schema],
        function_call=EnforcedFunctionCall(name="OutputSchema"),
    )

    gpt_request.add_system_message(system_content)
    gpt_request.update_max_token(
        DIRECTOR_MIN_TOKENS, DIRECTOR_PREFERRED_TOKENS)

    gpt_executor = GPTExecutor()

    for chunk in gpt_executor.execute(gpt_request):
        if chunk == "<<<< CLEAR >>>>":
            continue

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

        log.debug(text_chunk)
        await asyncio.sleep(0)

    full_result = gpt_executor.full_result
    tokens_used = gpt_executor.tokens_used

    if full_result.function_call is None:
        raise ValueError(
            f"Could not find function call in the text: {full_result}")

    raw_arguments = full_result.function_call["arguments"]
    arguments = json.loads(raw_arguments, strict=False)

    picked_agents = [
        agent for agent in available_agents if agent.id == arguments["agent_id"]]
    picked_agent = picked_agents[0] if picked_agents else None

    log.info(f"Chosen agent: {picked_agent}")

    if not picked_agent:
        log.error(f"Could not find agent in the text: {full_result}")
        picked_agent = available_agents[0]

    # TODO raw_arguments might not be accurate to check which manuals are needed
    relevant_manuals = [k for k in available_manuals if k.id in raw_arguments]

    task_context = ContentTaskContext(
        messages=request.messages,
        agent=picked_agent,
        relevant_manuals=relevant_manuals,
        mode=picked_agent.gpt_mode,
    )

    next_step = arguments["next_step"] if "next_step" in arguments else ""

    if picked_agent.id != "user":
        real_next_step = await rephrase_as_message_for_agent(messages, next_step=next_step, agent=picked_agent)
    else:
        real_next_step = ""

    analysis: DirectorResponse = {
        "next_step": real_next_step,
        "agent": AgentDict(
            **dict(
                picked_agent.model_dump()
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
        ]
    }
    log.debug(analysis)

    return analysis


"""
OmniTask.AI: "Omni" refers to all, which emphasizes the vast capabilities of AIConsole in managing diverse tasks. "Task.AI" reveals the product's function- to aid in executing tasks using AI.

Adapt.AI: An abbreviation for "Adaptable AI", this name emphasizes on AIConsole's adaptability to domain-specific functions. It's short and easy to remember, with a professional and modern feel to it.

Customix.AI: 
"""
