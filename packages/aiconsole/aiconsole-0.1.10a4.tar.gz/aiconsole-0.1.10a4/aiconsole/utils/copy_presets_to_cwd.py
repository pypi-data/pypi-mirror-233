import os
from importlib import resources
from shutil import copy2


def copy_presets_to_cwd(presets_dir):
    # Determine the path to the presets directory within the package
    full_path = f"aiconsole.presets.{presets_dir}"

    if os.path.exists(presets_dir):
        print(f"Presets directory '{presets_dir}' already exists, skipping copy")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(presets_dir):
        os.makedirs(presets_dir)

    # Iterate over the contents of the presets directory in the package
    for entry in resources.contents(full_path):
        
        # If the entry is a resource (i.e., a file), copy it
        if resources.is_resource(full_path, entry):
            with resources.path(full_path, entry) as source_path:
                print(source_path)
                # Copy each file to the current working directory
                copy2(source_path, os.path.join(presets_dir, entry))