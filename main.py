from fastapi import FastAPI
import uvicorn

from app.routers import api
from app.jobs.update_job import celery_app
from settings.config import ConfigService

app = FastAPI()

app.include_router(api)

# @app.on_event("startup")
# async def start_up():
#    celery_app.send_task("jobs.update_job.update_currency")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=ConfigService.HOST,
        port=ConfigService.PORT
    )
