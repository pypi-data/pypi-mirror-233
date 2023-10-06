"""

Sometimes openai returns wierd shit 

"""

import logging
import litellm
import tokentrim as tt
import json

from aiconsole.patched_interpreter.code_interpreters.language_map import language_map
from aiconsole.patched_interpreter.llm import setup_openai_coding_llm
from aiconsole.patched_interpreter.utils.convert_to_openai_messages import convert_to_openai_messages
from aiconsole.patched_interpreter.utils.display_markdown_message import display_markdown_message
from aiconsole.patched_interpreter.utils.merge_deltas import merge_deltas

log = logging.getLogger(__name__)

function_schema = {
  "name": "execute",
  "description":
  "Executes code on the user's machine, **in the users local environment**, and returns the output",
  "parameters": {
    "type": "object",
    "properties": {
      "language": {
        "type": "string",
        "description":
        "The programming language (required parameter to the `execute` function)",
        "enum": ["python", "R", "shell", "applescript", "javascript", "html"]
      },
      "code": {
        "type": "string",
        "description": "The code to execute (required)"
      }
    },
    "required": ["language", "code"]
  },
}

def parse_partial_json(s):

    # Attempt to parse the string as-is.
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
  
    # Initialize variables.
    new_s = ""
    stack = []
    is_inside_string = False
    escaped = False

    # Process each character in the string one at a time.
    for char in s:
        if is_inside_string:
            if char == '"' and not escaped:
                is_inside_string = False
            elif char == '\n' and not escaped:
                char = '\\n' # Replace the newline character with the escape sequence.
            elif char == '\\':
                escaped = not escaped
            else:
                escaped = False
        else:
            if char == '"':
                is_inside_string = True
                escaped = False
            elif char == '{':
                stack.append('}')
            elif char == '[':
                stack.append(']')
            elif char == '}' or char == ']':
                if stack and stack[-1] == char:
                    stack.pop()
                else:
                    # Mismatched closing character; the input is malformed.
                    return None
        
        # Append the processed character to the new string.
        new_s += char

    # If we're still inside a string at the end of processing, we need to close the string.
    if is_inside_string:
        new_s += '"'

    # Close any remaining open structures in the reverse order that they were opened.
    for closing_char in reversed(stack):
        new_s += closing_char

    # Attempt to parse the modified string as JSON.
    try:
        return json.loads(new_s)
    except json.JSONDecodeError:
        # If we still can't parse the string as JSON, return None to indicate failure.
        return s # AIConsole: return s instead of None

def patched_setup_openai_coding_llm(interpreter):
    """
    Takes an Interpreter (which includes a ton of LLM settings),
    returns a OI Coding LLM (a generator that takes OI messages and streams deltas with `message`, `language`, and `code`).
    """

    def coding_llm(messages):
        
        # Convert messages
        messages = convert_to_openai_messages(messages)

        # Add OpenAI's recommended function message
        messages[0]["content"] += "\n\nOnly use the function you have been provided with."

        # Seperate out the system_message from messages
        # (We expect the first message to always be a system_message)
        system_message = messages[0]["content"]
        messages = messages[1:]

        # Trim messages, preserving the system_message
        try:
            messages = tt.trim(messages=messages, system_message=system_message, model=interpreter.model)
        except:
            if interpreter.context_window:
                messages = tt.trim(messages=messages, system_message=system_message, max_tokens=interpreter.context_window)
            else:
                display_markdown_message("""
                **We were unable to determine the context window of this model.** Defaulting to 3000.
                If your model can handle more, run `interpreter --context_window {token limit}` or `interpreter.context_window = {token limit}`.
                """)
                messages = tt.trim(messages=messages, system_message=system_message, max_tokens=3000)

        if interpreter.debug_mode:
            print("Sending this to the OpenAI LLM:", messages)

        # Create LiteLLM generator
        params = {
            'model': interpreter.model,
            'messages': messages,
            'stream': True,
            'functions': [function_schema]
        }

        # Optional inputs
        if interpreter.api_base:
            params["api_base"] = interpreter.api_base
        if interpreter.api_key:
            params["api_key"] = interpreter.api_key
        if interpreter.max_tokens:
            params["max_tokens"] = interpreter.max_tokens
        if interpreter.temperature:
            params["temperature"] = interpreter.temperature
        
        # These are set directly on LiteLLM
        if interpreter.max_budget:
            litellm.max_budget = interpreter.max_budget
        if interpreter.debug_mode:
            litellm.set_verbose = True

        # Report what we're sending to LiteLLM
        if interpreter.debug_mode:
            print("Sending this to LiteLLM:", params)

        response = litellm.completion(**params)

        accumulated_deltas = {}
        language = None
        code = ""

        for chunk in response:
            if ('choices' not in chunk or len(chunk['choices']) == 0):
                # This happens sometimes
                continue

            delta = chunk["choices"][0]["delta"]

            # Accumulate deltas
            accumulated_deltas = merge_deltas(accumulated_deltas, delta)
            log.info("Accumulated deltas: %s", accumulated_deltas)

            if "content" in delta and delta["content"]:
                yield {"message": delta["content"]}

            
            if "function_call" in accumulated_deltas and "arguments" in accumulated_deltas["function_call"]:
                # This can now be both a string and a json object
                arguments = parse_partial_json(accumulated_deltas["function_call"]["arguments"])

                languages = language_map.keys()
                
                # AIConsole: We need to handle incorrect OpenAI responses
                if isinstance(arguments, str):
                    if language is None and "name" in accumulated_deltas["function_call"] and accumulated_deltas["function_call"]["name"] in languages:
                        language = accumulated_deltas["function_call"]["name"]
                        yield {"language": language}

                    if arguments and not arguments.startswith("{"):
                        if language is None:
                            language = "python"
                            yield {"language": language}

                        # Calculate the delta (new characters only)
                        code_delta = arguments[len(code):]
                        # Update the code
                        code = arguments
                        # Yield the delta
                        if code_delta:
                            yield {"code": code_delta}

                else:
                    if language is None and arguments and "language" in arguments and arguments["language"] in languages:
                        language = arguments["language"]
                        yield {"language": language}

                    if language is not None and arguments and "code" in arguments:
                        # Calculate the delta (new characters only)
                        code_delta = arguments["code"][len(code):]
                        # Update the code
                        code = arguments["code"]
                        # Yield the delta
                        if code_delta:
                            yield {"code": code_delta}
            
    return coding_llm

setup_openai_coding_llm.setup_openai_coding_llm = patched_setup_openai_coding_llm