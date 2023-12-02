from fastapi import APIRouter

from app.routers.service_routers import service

api = APIRouter(prefix="/api")

api.include_router(service)
