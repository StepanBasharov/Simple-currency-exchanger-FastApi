from fastapi import APIRouter

from app.schemas.exchange_schemas import ConvertRequest

exchange_router = APIRouter(prefix="/exchange")


@exchange_router.get("/last_db_update")
async def get_last_db_update():
    ...


@exchange_router.post("/convert")
async def convert(request: ConvertRequest):
    ...
