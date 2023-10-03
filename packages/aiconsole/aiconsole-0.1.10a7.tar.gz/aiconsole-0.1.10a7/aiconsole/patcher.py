import tokentrim
from typing import List, Dict, Any, Tuple, Optional, Union

"""

This is a bunch of monkey patches to the Open Interpreter codebase.

"""

def trim(
  messages: List[Dict[str, Any]],
  model = None,
  system_message: Optional[str] = None,
  trim_ratio: float = 0.75,
  return_response_tokens: bool = False,
  max_tokens = None
) -> Union[List[Dict[str, Any]], Tuple[List[Dict[str, Any]], int]]:
  """
  This function has an infinite loop bug in it. This is a patch to fix it.
  """

  if system_message:
    system_message_event = {"role": "system", "content": system_message}
    messages = [system_message_event] + messages

  return messages


def patch():
    tokentrim.trim = trim