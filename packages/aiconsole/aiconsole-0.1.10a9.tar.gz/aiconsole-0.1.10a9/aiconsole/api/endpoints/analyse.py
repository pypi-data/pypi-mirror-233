import logging

from fastapi import APIRouter
from aiconsole.director.DirectorResponse import DirectorResponse

from aiconsole.api.schema import AnalyseHTTPRequest
from aiconsole.director.director import director_analyse

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/analyse")
async def director(request: AnalyseHTTPRequest) -> DirectorResponse:
    return await director_analyse(request)
