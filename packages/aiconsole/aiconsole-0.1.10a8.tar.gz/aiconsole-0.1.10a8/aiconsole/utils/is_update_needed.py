import requests
import pkg_resources
from packaging import version

def is_update_needed():
    # Fetch the latest version from the PyPI API
    response = requests.get(f'https://pypi.org/pypi/aiconsole/json')
    latest_version = response.json()['info']['version']

    # Get the current version using pkg_resources
    current_version = pkg_resources.get_distribution("aiconsole").version

    return version.parse(latest_version) > version.parse(current_version)