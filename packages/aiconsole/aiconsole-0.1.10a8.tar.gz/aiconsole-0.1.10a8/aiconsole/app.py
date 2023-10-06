import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from aiconsole.agents.agents import agents
from aiconsole.api.routers import app_router
from aiconsole.manuals.manuals import manuals
from aiconsole.settings import settings, log_config
from aiconsole.utils.initialize_project_directory import initialize_project_directory

@asynccontextmanager
async def lifespan(app: FastAPI):
    manuals.reload()
    agents.reload()
    yield

logging.config.dictConfig(log_config)

def app_full():
    initialize_project_directory()


    app = FastAPI(title="AI Console", lifespan=lifespan)
    app.include_router(app_router)

    @app.get("/")
    def root():
        return FileResponse(os.path.join("./aiconsole/static", "index.html"))

    app.mount("/", StaticFiles(directory="./aiconsole/static"))

    return app

def app_only_backend():
    initialize_project_directory()


    app = FastAPI(title="AI Console Backend", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(app_router)

    return app


    