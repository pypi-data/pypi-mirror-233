import os
from importlib import resources
from shutil import copy2

PRESENT_PATH = "aiconsole.presets"


def copy_presets_to_cwd(presets_dir, path=PRESENT_PATH):
    # Determine the path to the present directory within the package
    full_path = f"{path}.{presets_dir}"

    if os.path.exists(presets_dir):
        print(f"Presets directory '{presets_dir}' already exists, skipping copy")
        return
    else:
        # Create the destination directory if it doesn't exist
        os.makedirs(presets_dir)

        # Iterate over the contents of the present directory in the package
        for entry in resources.contents(full_path):

            # If the entry is a resource (i.e., a file), copy it
            if resources.is_resource(full_path, entry):
                with resources.path(full_path, entry) as source_path:
                    # Copy each file to the current working directory
                    copy2(source_path, os.path.join(presets_dir, entry))
