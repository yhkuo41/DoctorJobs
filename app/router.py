from fastapi import APIRouter
from fastapi.responses import JSONResponse

index_router = APIRouter(tags=["Home"])


@index_router.get("/", response_class=JSONResponse)
async def home() -> JSONResponse:
    """Home Page"""
    message = {"message": "Hello! Here is DoctorJobs"}
    return JSONResponse(content=message)
