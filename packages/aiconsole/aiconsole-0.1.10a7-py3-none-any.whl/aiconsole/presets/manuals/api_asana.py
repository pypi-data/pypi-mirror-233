# Manual

import os
import json
from typing import Literal
import requests

def _get_personal_token():
    try:
        with open("./.aic/credentials/asana.json", "r") as f:
            # parse json
            personal_token = json.loads(f.read())["personal_token"]
    except FileNotFoundError:
        personal_token = None

    if not personal_token:
        raise Exception("Asana token not found. Please run `setup_asana` to set it up.")
    return personal_token

def _get_headers():
    return {
        'Authorization': f'Bearer {_get_personal_token()}',
    }


def _get_workspace():
    try:
        with open("./.aic/credentials/asana.json", "r") as f:
            # parse json
            workspace = json.loads(f.read())["workspace"]
    except FileNotFoundError:
        workspace = None

    if not workspace:
        raise Exception("Asana workspace not found. Please run `set_workspace` to set it up.")
    return workspace


def setup(personal_token: str):
    os.makedirs("./.aic/credentials", exist_ok=True)

    with open("./.aic/credentials/asana.json", "w") as f:
        f.write(json.dumps({
            "personal_token": personal_token,
            "workspace": ""
        }))

    print ("Asana setup complete. Next step is to use set_workspace.")

def set_workspace(workspace: str):
    with open("./.aic/credentials/asana.json", "r") as f:
        # parse json
        data = json.loads(f.read())
        data["workspace"] = workspace

    with open("./.aic/credentials/asana.json", "w") as f:
        f.write(json.dumps(data))

def add_task(task: str):
    response = requests.post('https://app.asana.com/api/1.0/tasks', headers=_get_headers(), json={
        'data': {
            'assignee': 'me',
            'workspace': _get_workspace(),
            'name': task,
        }
    }
)
    print(response.status_code, response.json())

def get_tasks(assignee_gid: str | Literal['me'] | None = None, completed_since: str | Literal["now"] | None = None, modified_since:str | Literal["now"] | None = None):
    # Each of these parameters is an optional filter.
    # Note that parameters are passed directly into the `params` argument of `requests.get`.
    # Remember that for the Asana API, 'now' means tasks that are either incomplete or were completed in the last week. For time specific timestamps, they have to be in RFC3339 format, e.g., 2008-01-14T04:02:59Z.
    params = {
        'assignee': assignee_gid,
        'completed_since': completed_since,
        'modified_since': modified_since,
    }

    # Use the params argument to send these parameters in the GET request.
    response = requests.get(
        'https://app.asana.com/api/1.0/tasks', headers=_get_headers(), params=params)

    # Get tasks from the response.
    tasks = response.json().get('data', [])
    
    return tasks

def delete_task(task_id: str):
    response = requests.delete(f'https://app.asana.com/api/1.0/tasks/{task_id}', headers=_get_headers())
    return response.json()

# The `update` parameter should be a dictionary containing fields that you want to update
# For example: update = {"name": "New task name", assignee: 'newuser'}
def update_task(task_id: str, update: dict):
    data = {"data": update}
    response = requests.put(f'https://app.asana.com/api/1.0/tasks/{task_id}', headers=_get_headers(), json=data)
    return response.json()

def mark_task_completed(task_id: str):
    return update_task(task_id, {"completed": True})

def assign_task_to(task_id: str, assignee: str):
    return update_task(task_id, {"assignee": assignee})


manual = {
    "usage": "Use this when you need to access my asana",
    "content": lambda context: """

# Asana Usage Manual

Assume that you already have the access token and try to execute, only ask about setup if it fails.

example of code:
```python
import api_asana
api_asana.add_task('Do dishes')


params = {'assignee': 'me', 'workspace': '1155412040978277', 'limit': 10}
response = requests.get('https://app.asana.com/api/1.0/tasks', headers=headers, params=params)
(response.status_code, response.json())
```

documentation for module api_asana:
```python
def setup(personal_token: str)

def set_workspace(workspace: str)

def add_task(task: str)

# Each of these parameters is an optional filter.
# Note that parameters are passed directly into the `params` argument of `requests.get`.
# Remember that for the Asana API, 'now' means tasks that are either incomplete or were completed in the last week. 
def get_tasks(assignee_gid: str | Literal['me'] | None = "me", completed_since: str | Literal["now"] | None ="now", modified_since:str | Literal["now"] | None = None)

def delete_task(task_id: str)

# The `update` parameter should be a dictionary containing fields that you want to update
# For example: update = {"name": "New task name", assignee: 'newuser'}
def update_task(task_id: str, update: dict)

def mark_task_completed(task_id: str)

def assign_task_to(task_id: str, assignee: str)

""".strip(),
}
