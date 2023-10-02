import json
import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from aiconsole.api.schema import CommandHistoryPostRequest

router = APIRouter()

COMMAND_HISTORY_LIMIT = 1000

@router.get("/commands_history")
def get_history():
    if not os.path.exists(f"./.aic/command_history.json"):
        return JSONResponse([])

    with open(f"./.aic/command_history.json", "r") as f:
        commands = json.load(f)
    return JSONResponse(commands)

@router.post("/commands_history")
def save_history(request: CommandHistoryPostRequest):
    """
    Saves the history of send commands to ./aic/history/{conversation_id}.json
    """

    os.makedirs("./.aic", exist_ok=True)

    #read
    if not os.path.exists(f"./.aic/command_history.json"):
        commands = []
    else:
        with open(f"./.aic/command_history.json", "r") as f:
            commands = json.load(f)

    commands.append(request.command)

    #remove non unique but keep the order
    commands.reverse()
    commands = list(dict.fromkeys(commands))
    commands.reverse()

    #limit
    commands = commands[-COMMAND_HISTORY_LIMIT:]

    #write
    with open(f"./.aic/command_history.json", "w") as f:
        json.dump(commands, f, indent=4)

    return JSONResponse(commands)