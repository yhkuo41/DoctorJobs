from typing import Callable
from urllib.parse import parse_qsl, urlencode

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse

from app.auth.router import auth_router
from app.db.database import mongo_client
from app.job_msg.line_job_msg_router import job_msg_line_router
from app.job_msg.router import job_msg_router
from app.router import index_router
from app.user.router import user_router

app = FastAPI(
    title="DoctorJobs",
    description="A service that collects and provides access to doctor job information",
    version="1.0.0",
    contact={
        "name": "Y.H. Kuo",
        "email": "yhkuo41@gmail.com",
    },
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(index_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(job_msg_router)
app.include_router(job_msg_line_router)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.middleware("http")
async def filter_blank_query_params(request: Request, call_next: Callable):
    scope = request.scope
    if scope and scope.get("query_string"):
        filtered_query_params = parse_qsl(
            qs=scope["query_string"].decode("latin-1"),
            keep_blank_values=False,
        )
        scope["query_string"] = urlencode(filtered_query_params).encode("latin-1")
    return await call_next(request)


@app.on_event("shutdown")
def shutdown_event():
    mongo_client.close()


if __name__ == "__main__":
    # Local WSGI: Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
