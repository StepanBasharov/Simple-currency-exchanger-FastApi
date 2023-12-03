from fastapi import FastAPI
import uvicorn

from app.routers import api
from settings.config import ConfigService

app = FastAPI()

app.include_router(api)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=ConfigService.HOST,
        port=ConfigService.PORT
    )
