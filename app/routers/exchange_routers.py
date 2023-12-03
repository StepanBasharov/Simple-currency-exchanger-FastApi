from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.exchange_schemas import ConvertRequest
from app.models.exchange_models import ExchangeCurrency
from app.utils.database import get_session

exchange_router = APIRouter(prefix="/exchange")


@exchange_router.get("/last_db_update")
async def get_last_db_update(session: AsyncSession = Depends(get_session)):
    data = select(ExchangeCurrency)
    data = await session.execute(data)
    data = data.scalars().all()
    print(data)
    return "OK"


@exchange_router.post("/convert")
async def convert(request: ConvertRequest):
    ...
