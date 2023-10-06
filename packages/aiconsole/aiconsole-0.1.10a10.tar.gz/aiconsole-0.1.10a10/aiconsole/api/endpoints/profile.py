from importlib import resources
import logging
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

from aiconsole.settings import AGENTS_CORE_RESOURCE, AGENTS_DIRECTORY

router = APIRouter()

log = logging.getLogger(__name__)

@router.get("/profile/{image}")
async def profile_image(image: str):
    if os.path.exists(os.path.join(AGENTS_DIRECTORY, image)):
        return FileResponse(os.path.join(AGENTS_DIRECTORY, image))
    
    path = resources.path(AGENTS_CORE_RESOURCE, image)
    return FileResponse(str(path))