import asyncio
from typing import List
from aiconsole.aic_types import Agent
from aiconsole.gpt.consts import GPTMode
from aiconsole.gpt.gpt_executor import GPTExecutor
from aiconsole.gpt.gpt_types import GPTMessage
from aiconsole.gpt.request import GPTRequest
import logging

log = logging.getLogger(__name__)

async def rephrase_as_message_for_agent(history: List[GPTMessage], next_step: str, agent: Agent) -> str:
    system_content = f"""
You are a director of a multiple AI Agents, doing everything to help the user.
You have multiple AI Agents at your disposal, each with their own unique capabilities.
Some of them can run code on this local machine in order to perform any tasks that the user needs.

Your job is to delegate a task to one of your agents, and make sure that the user gets the best experience possible.

Tell "{agent.name}" to do whatever is needed in order to achive the next action item:

```text
{next_step}.
```

Answer with only with your direction, directed to "{agent.name}" (Agent description: "{agent.usage}").

Make sure to mention that agent by name.

Make sure that your answer is no longer than 100 characters.

Remove any formatting, such as markdown, from your answer. This is a simple chat message.
"""

    request = GPTRequest(
        messages=history,
        mode= GPTMode.FAST,
    )
    
    request.add_system_message(system_content)
    request.update_max_token(100, 200)

    gpt_executor = GPTExecutor()

    for chunk in gpt_executor.execute(request):
        await asyncio.sleep(0)
    
    return gpt_executor.full_result.content if gpt_executor.full_result else ""


async def rephrase_as_message_for_user(history: List[GPTMessage], next_step: str, agent: Agent) -> str:
    system_content = f"""
You are a director of a multiple AI Agents, doing everything to help the user.
You have multiple AI Agents at your disposal, each with their own unique capabilities.
Some of them can run code on this local machine in order to perform any tasks that the user needs.

The next action is on the user. Tell the user ({agent.name}) whatever whatever is appropriate related to the established next step: {next_step}.

Keep in mind that the user has seenthe last answer of your agent, so don't repeat information from it.

Make sure that your answer is no longer than 100 characters.

Remove any formatting, such as markdown, from your answer. This is a simple chat message.
"""

    request = GPTRequest(
        messages=history,
        mode= GPTMode.FAST,
    )
    
    request.add_system_message(system_content)
    request.update_max_token(100, 200)

    gpt_executor = GPTExecutor()

    for chunk in gpt_executor.execute(request):
        await asyncio.sleep(0)
    
    return gpt_executor.full_result.content if gpt_executor.full_result else ""
