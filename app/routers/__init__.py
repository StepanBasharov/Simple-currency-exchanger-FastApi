from fastapi import APIRouter

from app.routers.service_routers import service_router
from app.routers.exchange_routers import exchange_router

# Основной роутер
api = APIRouter(prefix="/api")

# Добавление сервисных роутеров
api.include_router(service_router)

# Добавляем роутер для работы с валютами
api.include_router(exchange_router)
