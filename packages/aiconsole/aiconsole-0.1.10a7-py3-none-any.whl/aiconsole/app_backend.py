from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiconsole.api.routers import app_router
from aiconsole.settings import settings
from aiconsole.manuals import manuals
from aiconsole.agents import agents

from aiconsole import patcher

patcher.patch()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router)

manuals.reload()
agents.reload()
