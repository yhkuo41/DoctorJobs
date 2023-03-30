import uvicorn
from fastapi import FastAPI

from app.auth.router import auth
from app.db.db import mongo_client
from app.job_msg.router import job_msg
from app.router import index
from app.user.router import user

app = FastAPI(
    title="DoctorJobs",
    description="A service that collects and provides access to doctor job information",
    version="1.0.0",
    contact={
        "name": "Y.H. Kuo",
        "email": "yhkuo41@gmail.com",
    },
)

app.include_router(index)
app.include_router(job_msg)
app.include_router(user)
app.include_router(auth)


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
