from datetime import datetime

from fastapi import APIRouter

from app.schemas.service_schemas import PingResponse

service = APIRouter(prefix="/service")


@service.get("/ping")
async def ping():
    return PingResponse(message="PONG", time=datetime.utcnow())
