import importlib.util
import logging
import os
from typing import Dict

import watchdog.events
import watchdog.observers

from aiconsole.aic_types import Agent
from aiconsole.execution_modes.interpreter import execution_mode_interpreter
from aiconsole.execution_modes.normal import execution_mode_normal
from aiconsole.gpt.consts import GPTMode
from aiconsole.settings import AGENTS_CORE_RESOURCE, AGENTS_DIRECTORY, DEFAULT_MODE
from aiconsole.utils.list_files_in_file_system import list_files_in_file_system
from aiconsole.utils.list_files_in_resource_path import list_files_in_resource_path

log = logging.getLogger(__name__)

class Agents:
    """
    Agents class is for managing the .md and .py agent files.
    """

    agents: Dict[str, Agent]

    def __init__(self):
        self.agents = {}

        observer = watchdog.observers.Observer()

        parent = self

        class Handler(watchdog.events.FileSystemEventHandler):
            def on_modified(self, event):
                if event.is_directory or not event.src_path.endswith(".py"):
                    return
                parent.reload()

        observer.schedule(Handler(), AGENTS_DIRECTORY, recursive=True)

        observer.start()

    def all_agents(self):
        """
        Return all loaded materials.
        """
        return list(self.agents.values())

    def reload(self):
        log.info("Reloading agents ...")

        execution_modes = {
            "interpreter": execution_mode_interpreter,
            "normal": execution_mode_normal,
        }

        self.agents = {}

        paths = [path for paths_yielding_function in [
            list_files_in_resource_path(AGENTS_CORE_RESOURCE),
            list_files_in_file_system(AGENTS_DIRECTORY)
        ] for path in paths_yielding_function]

        for path in paths:
            filename = os.path.basename(path)
            if filename.endswith(".py"):
                # Check if the first line of the file is '# Agent'
                with open(path, "r") as file:
                    first_line = file.readline().strip()
                    if first_line != "# Agent":
                        log.warning(
                            f"Skipping invalid agent in file {filename}")
                        continue

                # Import the file and execute manual function to get the manual
                module_name = os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(
                    module_name, path)
                if not spec or spec.loader is None:
                    log.warning(f"Skipping invalid agent in file {filename}")
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                agent = module.agent
                id = filename[:-3]
                if id in self.agents:
                    log.warning(
                        f"Skipping duplicate agent {id} in file {filename}")
                    continue

                gpt_mode_raw = agent["gpt_mode"] if "gpt_mode" in agent else None

                if gpt_mode_raw == 'QUALITY':
                    gpt_mode = GPTMode.QUALITY
                elif gpt_mode_raw == 'FAST':
                    gpt_mode = GPTMode.FAST
                else:
                    gpt_mode = DEFAULT_MODE
                
                self.agents[id] = Agent(
                    id=id,
                    name=agent["name"],
                    usage=agent["usage"],
                    system=agent["system"],
                    execution_mode=execution_modes[agent["execution_mode"]],
                    gpt_mode = gpt_mode,
                )

        log.info(f"Reloaded {len(self.agents)} agents")


agents = Agents()
