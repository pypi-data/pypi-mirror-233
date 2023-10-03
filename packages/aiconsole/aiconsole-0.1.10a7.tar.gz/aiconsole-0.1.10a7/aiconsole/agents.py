import importlib.util
import os
import sys
from typing import Dict
import watchdog.observers
import watchdog.events
from aiconsole.aic_types import Agent
from aiconsole.utils.copy_presets_to_cwd import copy_presets_to_cwd
from aiconsole.execution_modes.interpreter import execution_mode_interpreter
from aiconsole.execution_modes.normal import execution_mode_normal

AGENTS_DIRECTORY = "agents"


class Agents:
    """
    Agents class is for managing the .md and .py agent files.
    """

    agents: Dict[str, Agent]

    def __init__(self):
        self.agents = {}

        copy_presets_to_cwd(AGENTS_DIRECTORY)

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
        print("Reloading agents ...")

        execution_modes = {
            "interpreter": execution_mode_interpreter,
            "normal": execution_mode_normal,
        }

        self.agents = {}
        for filename in os.listdir(AGENTS_DIRECTORY):
            if filename.endswith(".py"):
                # Check if the first line of the file is '# Agent'
                with open(os.path.join(AGENTS_DIRECTORY, filename), "r") as file:
                    first_line = file.readline().strip()
                    if first_line != "# Agent":
                        print(f"Skipping invalid agent in file {filename}")
                        continue

                # Import the file and execute manual function to get the manual
                path = os.path.join(AGENTS_DIRECTORY, filename)
                module_name = os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(module_name, path)
                if not spec or spec.loader is None:
                    print(f"Skipping invalid agent in file {filename}")
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                agent = module.agent
                id = filename[:-3]
                if id in self.agents:
                    print(f"Skipping duplicate agent {id} in file {filename}")
                    continue
                self.agents[id] = Agent(
                    id=id,
                    name=agent["name"],
                    usage=agent["usage"],
                    system=agent["system"],
                    execution_mode=execution_modes[agent["execution_mode"]],
                )

        print(f"Reloaded {len(self.agents)} agents")


agents = Agents()
