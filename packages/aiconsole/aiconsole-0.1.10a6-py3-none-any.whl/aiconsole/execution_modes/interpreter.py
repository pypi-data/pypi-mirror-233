import asyncio
from typing import AsyncGenerator
from aiconsole.aic_types import ExecutionTaskContext
from aiconsole.gpt.create_full_prompt_from_sections import (
    create_full_prompt_from_sections,
)
from aiconsole.code_interpreter.core.core import Interpreter
from aiconsole.code_interpreter.llm.setup_llm import setup_llm

interpreter = Interpreter()
interpreter.debug_mode = False
interpreter.model = "gpt-4"


async def execution_mode_interpreter(
    context: ExecutionTaskContext,
) -> AsyncGenerator[str, None]:

    # Setup the LLM
    if not interpreter._llm:
        interpreter._llm = setup_llm(interpreter)

    interpreter.system_message = create_full_prompt_from_sections(
        intro=context.agent.system,
        sections=context.relevant_manuals,
        outro="\n\n---\n\n",
    )

    print("System message:")
    print(interpreter.system_message)

    interpreter.messages = [
        {"role": message.role, "message": message.content}
        for message in context.messages
    ]

    in_code = False
    in_code_output = False

    for chunk in interpreter._respond():
        print(chunk)

        try:
            if not chunk.get("output", ""):
                if in_code_output:
                    yield f'<<<< END CODE OUTPUT >>>>'
                    in_code_output = False

            if not chunk.get("code", "") and not chunk.get("language", ""):
                if in_code:
                    yield f'<<<< END CODE >>>>'
                    in_code = False

            if chunk.get("language", ""):
                if in_code_output:
                    raise Exception("Language inside output")
                if not in_code:
                    yield f'<<<< START CODE ({str(chunk.get("language", ""))}) >>>>'
                in_code = True
            
            if chunk.get("code", ""):
                if in_code_output:
                    raise Exception("Code inside output")
                
                if not in_code:
                    raise Exception("Code without language")
                yield str(chunk.get("code", ""))

            if chunk.get("output", ""):
                if in_code:
                    raise Exception("Output inside code")
                
                if not in_code_output:
                    yield f'<<<< START CODE OUTPUT >>>>'
                in_code_output = True

                yield str(chunk.get("output", ""))
            
            if chunk.get("message", ""):
                if in_code:
                    yield f'<<<< END CODE >>>>'
                in_code = False
                in_code_output = False
                yield str(chunk.get("message", ""))

            await asyncio.sleep(0)
        except asyncio.CancelledError:
            print("Cancelled")
            break
