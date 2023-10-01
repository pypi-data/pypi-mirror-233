import json
import os

from fastapi import APIRouter
from aiconsole.api.schema import BaseGptHTTPRequest
from datetime import datetime

router = APIRouter()


@router.post("/chats_history")
def save_history(request: BaseGptHTTPRequest):
    """
    Saves the history of the conversation to ./aic/history/{conversation_id}.json
    """

    os.makedirs("./.aic/history", exist_ok=True)

    with open(f"./.aic/history/{request.conversation_id}.json", "w") as f:
        json.dump({
            "conversation_id": request.conversation_id,
            "timestamp": datetime.now().isoformat(),
            "messages": [message.model_dump() for message in request.messages]
        }, f, indent=4)