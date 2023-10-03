from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/profile/{image}")
async def profile_image(image: str):
    return FileResponse(f"./agents/{image}")