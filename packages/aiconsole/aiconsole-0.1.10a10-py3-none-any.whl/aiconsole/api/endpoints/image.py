import logging
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

log = logging.getLogger(__name__)

@router.get("/image")
async def image(path: str):
    #get parameter path
    return FileResponse(os.path.join(os.getcwd(), path))