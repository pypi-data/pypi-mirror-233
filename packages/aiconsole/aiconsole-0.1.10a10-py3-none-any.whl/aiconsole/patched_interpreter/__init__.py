"""

This is a bunch of monkey patches to the Open Interpreter codebase.
This approach allows for updates to the Open Interpreter codebase without having to manually merge changes.

Only this file is actually modified: removed spawning an instance of interpreter, this needs to be fixed inline here

"""
from .patches import patch_get_relevant_procedures
from .patches import patch_check_for_update
from .patches import patch_language_python
from .patches import patch_setup_openai_coding_llm
from .patches import patch_subprocess_code_interpreter
from .patches import patch_trim

# from .core.core import Interpreter
# import sys

# This is done so when users `import interpreter`,
# they get an instance of interpreter:

#sys.modules["interpreter"] = Interpreter()

# **This is a controversial thing to do,**
# because perhaps modules ought to behave like modules.

# But I think it saves a step, removes friction, and looks good.

#     ____                      ____      __                            __           
#    / __ \____  ___  ____     /  _/___  / /____  _________  ________  / /____  _____
#   / / / / __ \/ _ \/ __ \    / // __ \/ __/ _ \/ ___/ __ \/ ___/ _ \/ __/ _ \/ ___/
#  / /_/ / /_/ /  __/ / / /  _/ // / / / /_/  __/ /  / /_/ / /  /  __/ /_/  __/ /    
#  \____/ .___/\___/_/ /_/  /___/_/ /_/\__/\___/_/  / .___/_/   \___/\__/\___/_/     
#      /_/                                         /_/                               