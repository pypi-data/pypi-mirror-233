"""

We want to add our own imports of manuals and agents

"""

from importlib import resources

from aiconsole.settings import AGENTS_DIRECTORY, MANUALS_DIRECTORY
from ..code_interpreters.languages import python
from ..code_interpreters.languages.python import wrap_in_try_except, add_active_line_prints


def preprocess_python(code):
    """
    Add active line markers
    Wrap in a try except
    Add end of execution marker
    """

    # AIConsole Fix: We want to add our own imports
    code = f"""
import sys
import os

sys.path.append('{resources.path('aiconsole.manuals', 'core')}')
sys.path.append('{resources.path('aiconsole.agents', 'core')}')
sys.path.append('{MANUALS_DIRECTORY}')
sys.path.append('{AGENTS_DIRECTORY}')
""".strip() + "\n" + code
    
    print(code)


    # Add print commands that tell us what the active line is
    code = add_active_line_prints(code)

    # Wrap in a try except
    code = wrap_in_try_except(code)

    # Remove any whitespace lines, as this will break indented blocks
    # (are we sure about this? test this)
    code_lines = code.split("\n")
    code_lines = [c for c in code_lines if c.strip() != ""]
    code = "\n".join(code_lines)

    # Add end command (we'll be listening for this so we know when it ends)
    code += '\n\nprint("## end_of_execution ##")'

    return code


python.preprocess_python = preprocess_python
