from datetime import datetime

from fastapi import APIRouter

from app.schemas.service_schemas import PingResponse

service_router = APIRouter(prefix="/service")


@service_router.get("/ping")
async def ping():
    """ Эндпоинт для проверки работоспособности сервиса"""
    return PingResponse(message="PONG", time=datetime.utcnow())
