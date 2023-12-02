from fastapi import APIRouter

from app.routers.service_routers import service_router

# Основной роутер
api = APIRouter(prefix="/api")

# Добавление сервисных роутеров
api.include_router(service_router)
