import logging
import os
from datetime import datetime
from typing import Callable

from fastapi import APIRouter, status, Response, Depends

from aiconsole.api.json_file_operations import json_read, json_write
from aiconsole.api.schema import ConversationHistoryHTTPRequest
from aiconsole.settings import settings

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/chats/history/{conversation_id}")
def get_history(conversation_id: str, get_json: Callable = Depends(json_read)):
    file_path = os.path.join(settings.HISTORY_DIRECTORY, f"{conversation_id}.json")

    return get_json(file_path=file_path, empty_obj={})


@router.post("/chats/history")
def save_history(request: ConversationHistoryHTTPRequest, store_json: Callable = Depends(json_write)):
    """
    Saves the history of the conversation to <history_dir>/<request.conversation_id>.json
    """

    conversation_data = {
        "conversation_id": request.conversation_id,
        "timestamp": datetime.now().isoformat(),
        "messages": [message.model_dump() for message in request.messages]
    }
    store_json(
        directory=settings.HISTORY_DIRECTORY,
        file_name=f"{request.conversation_id}.json",
        content=conversation_data
    )
    return Response(
        status_code=status.HTTP_201_CREATED,
        content="Chat history saved successfully",
    )


@router.get("/chats/headlines")
def get_history_headlines(get_json: Callable = Depends(json_read)):
    history_directory = settings.HISTORY_DIRECTORY
    headlines = []
    if os.path.exists(history_directory) and os.path.isdir(history_directory):
        for file_name in os.listdir(history_directory):
            if file_name.endswith(".json"):
                file_path = os.path.join(history_directory, file_name)
                history = get_json(file_path=file_path, empty_obj={})

                if history:
                    try:
                        for msg in history.get("messages"):
                            if msg.get("role") == "user":
                                first_msg = msg.get("content")
                                headlines.append({
                                    "message": first_msg, 
                                    "conversation_id": history.get("conversation_id")
                                })
                                break  # Exit the loop after finding the first user message

                    except Exception as e:
                        log.exception(f"Failed to get history: {e}")
                        return "Failed to get history"

    if headlines:
        return headlines
    else:
        return "No history found"
