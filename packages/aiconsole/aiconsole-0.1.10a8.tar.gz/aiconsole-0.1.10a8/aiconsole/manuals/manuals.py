from importlib import resources
import importlib.util
import logging
import os
import re
from typing import Dict

import watchdog.events
import watchdog.observers

from aiconsole.aic_types import Manual
from aiconsole.settings import MANUALS_CORE_RESOURCE, MANUALS_DIRECTORY
from aiconsole.manuals.documentation_from_code import documentation_from_code
from aiconsole.utils.list_files_in_file_system import list_files_in_file_system
from aiconsole.utils.list_files_in_resource_path import list_files_in_resource_path

log = logging.getLogger(__name__)


class Manuals:
    """
    Manuals' class is for managing the .md and .py manual files.
    """

    manuals: Dict[str, Manual]

    def __init__(self):
        self.manuals = {}

        observer = watchdog.observers.Observer()

        parent = self

        class Handler(watchdog.events.FileSystemEventHandler):
            def on_modified(self, event):
                if event.is_directory or (
                    not event.src_path.endswith(".py")
                    and not event.src_path.endswith(".md")
                ):
                    return
                parent.reload()

        observer.schedule(Handler(), MANUALS_DIRECTORY, recursive=True)
        observer.start()

    def all_manuals(self):
        """
        Return all loaded materials.
        """
        return list(self.manuals.values())

    def delete_manual(self, name):
        """
        Delete a specific material.
        """
        if name not in self.manuals:
            raise KeyError(f"Material {name} not found")
        del self.manuals[name]

    def reload(self):
        log.info("Reloading manuals ...")

        self.manuals = {}

        paths = [path for paths_yielding_function in [
            list_files_in_resource_path(MANUALS_CORE_RESOURCE),
            list_files_in_file_system(MANUALS_DIRECTORY)
        ] for path in paths_yielding_function]

        for path in paths:
            filename = os.path.basename(path)
            if filename.endswith(".py"):
                # Check if the first line of the file is '# Manual'
                with open(path, "r") as file:
                    first_line = file.readline().strip()
                    if first_line != "# Manual":
                        log.warning(
                            f"Skipping invalid manual in file {filename}")
                        continue

                # Import the file and execute manual function to get the manual
                module_name = os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(
                    module_name, path)
                if not spec or spec.loader is None:
                    log.warning(f"Skipping invalid manual in file {filename}")
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                manual = module.manual
                id = filename[:-3]
                if id in self.manuals:
                    log.warning(
                        f"Skipping duplicate manual {id} in file {filename}")
                    continue

                if "content" not in manual:
                    manual["content"] = documentation_from_code(module_name, path)
            
                self.manuals[id] = Manual(
                    id=id, usage=manual["usage"], content=manual["content"]
                )
            elif filename.endswith(".md"):
                with open(path, "r") as file:
                    lines = file.readlines()

                    # Merging all lines into a single string
                    text = "".join(lines)

                    pattern = r"\s*(<!---|<!--)\s*(.*?)\s*(-->)\s*(.*)\s*"

                    match = re.match(pattern, text.strip(), re.DOTALL)

                    if not match:
                        log.warning(
                            f"Skipping invalid manual in file {filename}")
                        continue

                    # Extracting 'usage' and 'content' based on matched groups
                    usage = match.group(2)
                    content = match.group(4)

                    # Pruning leading/trailing spaces and newlines (if any)
                    usage = usage.strip()
                    content = content.strip()

                    manual_id = os.path.splitext(filename)[0]
                    if manual_id in self.manuals:
                        log.warning(
                            f"Skipping duplicate manual {manual_id} in file {filename}"
                        )
                        continue

                    self.manuals[manual_id] = Manual(
                        id=manual_id,
                        usage=usage,
                        content=lambda context, content=content: content,
                    )

        log.info(f"Reloaded {len(self.manuals)} manuals")


manuals = Manuals()
