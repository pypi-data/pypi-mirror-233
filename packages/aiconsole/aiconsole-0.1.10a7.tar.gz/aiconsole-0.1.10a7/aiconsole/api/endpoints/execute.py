from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from aiconsole.aic_types import ExecutionTaskContext
from aiconsole.api.schema import ExecuteHTTPRequest
from aiconsole.agents import agents

router = APIRouter()


@router.post("/execute")
async def execute(request: ExecuteHTTPRequest) -> StreamingResponse:
    agent = agents.agents[request.agent]

    context = ExecutionTaskContext(
        messages=request.messages,
        agent=agent,
        relevant_manuals=request.relevant_manuals,
        mode=request.mode,
    )

    return StreamingResponse(
        agent.execution_mode(context), media_type="text/event-stream"
    )
