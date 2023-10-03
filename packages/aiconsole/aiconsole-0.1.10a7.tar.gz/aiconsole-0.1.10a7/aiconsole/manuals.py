import importlib.util
import os
import sys
from typing import Dict
import watchdog.observers
import watchdog.events
import re
import os

from aiconsole.aic_types import Manual
from aiconsole.utils.copy_presets_to_cwd import copy_presets_to_cwd

MANUALS_DIRECTORY = "manuals"

class Manuals:
    """
    Manuals class is for managing the .md and .py manual files.
    """

    manuals: Dict[str, Manual]

    def __init__(self):
        self.manuals = {}

        copy_presets_to_cwd(MANUALS_DIRECTORY)

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
        print("Reloading manuals ...")

        self.manuals = {}
        for filename in os.listdir(MANUALS_DIRECTORY):
            if filename.endswith(".py"):
                # Check if the first line of the file is '# Manual'
                with open(os.path.join(MANUALS_DIRECTORY, filename), "r") as file:
                    first_line = file.readline().strip()
                    if first_line != "# Manual":
                        print(f"Skipping invalid manual in file {filename}")
                        continue

                # Import the file and execute manual function to get the manual
                path = os.path.join(MANUALS_DIRECTORY, filename)
                module_name = os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(module_name, path)
                if not spec or spec.loader is None:
                    print(f"Skipping invalid manual in file {filename}")
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                manual = module.manual
                id = filename[:-3]
                if id in self.manuals:
                    print(
                        f"Skipping duplicate manual {id} in file {filename}"
                    )
                    continue
                self.manuals[id] = Manual(
                    id=id, usage=manual["usage"], content=manual["content"]
                )
            elif filename.endswith(".md"):
                path = os.path.join(MANUALS_DIRECTORY, filename)
                with open(path, "r") as file:
                    lines = file.readlines()

                    # Merging all lines into a single string
                    text = "".join(lines)

                    pattern = r"\s*(<!---|<!--)\s*(.*?)\s*(-->)\s*(.*)\s*"

                    match = re.match(pattern, text.strip(), re.DOTALL)

                    if not match:
                        print(f"Skipping invalid manual in file {filename}")
                        continue

                    # Extracting 'usage' and 'content' based on matched groups
                    usage = match.group(2)
                    content = match.group(4)

                    # Pruning leading/trailing spaces and newlines (if any)
                    usage = usage.strip()
                    content = content.strip()

                    manual_id = os.path.splitext(filename)[0]
                    if manual_id in self.manuals:
                        print(
                            f"Skipping duplicate manual {manual_id} in file {filename}"
                        )
                        continue

                    self.manuals[manual_id] = Manual(
                        id=manual_id,
                        usage=usage,
                        content=lambda context, content=content: content,
                    )

        print(f"Reloaded {len(self.manuals)} manuals")


manuals = Manuals()
