from fastapi import APIRouter

from aiconsole.api.endpoints import analyse, chats_history, commands_history, execute, profile

app_router = APIRouter()

app_router.include_router(analyse.router, tags=["analyse"])
app_router.include_router(execute.router, tags=["execute"])
app_router.include_router(profile.router, tags=["profile"])
app_router.include_router(chats_history.router, tags=["profile"])
app_router.include_router(commands_history.router, tags=["profile"])
