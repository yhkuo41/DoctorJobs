from fastapi import APIRouter
from fastapi.responses import JSONResponse

index = APIRouter()


@index.get("/", response_class=JSONResponse)
async def home() -> JSONResponse:
    """Home Page
    Returns:
        JSONResponse: Hello!
    """
    message = {"message": "Hello! Here is DoctorJobs"}
    return JSONResponse(content=message)
