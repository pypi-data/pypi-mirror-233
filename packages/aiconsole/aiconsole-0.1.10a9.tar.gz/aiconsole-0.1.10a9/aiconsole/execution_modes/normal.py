import asyncio
import logging
from typing import AsyncGenerator

from aiconsole.aic_types import ExecutionTaskContext
from aiconsole.gpt.consts import GPTMode
from aiconsole.gpt.create_full_prompt_from_sections import \
    create_full_prompt_from_sections
from aiconsole.gpt.gpt_executor import GPTExecutor
from aiconsole.gpt.request import GPTRequest

MIN_TOKENS = 250
PREFERRED_TOKENS = 2000

log = logging.getLogger(__name__)


async def execution_mode_normal(
    context: ExecutionTaskContext,
) -> AsyncGenerator[str, None]:
    log.debug("execution_mode_normal")

    system_content = create_full_prompt_from_sections(
        intro=context.agent.system,
        sections=context.relevant_manuals,
        outro="\n\n---\n\n",
    )

    request = GPTRequest(
        messages=context.messages,
        mode=context.mode,
    )
    request.add_system_message(system_content)
    request.update_max_token(MIN_TOKENS, PREFERRED_TOKENS)

    gpt_executor = GPTExecutor()

    for chunk in gpt_executor.execute(request):
        try:
            yield chunk["choices"][0]["delta"].get("content", "")
            await asyncio.sleep(0)
        except asyncio.CancelledError:
            log.warning("Cancelled execution_mode_normal")
            break
