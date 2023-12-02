from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.exchange_schemas import ConvertRequest
from app.models.exchange_models import ExchangeCurrency
from app.utils.database import get_session

exchange_router = APIRouter(prefix="/exchange")


@exchange_router.get("/last_db_update")
async def get_last_db_update(session: AsyncSession = Depends(get_session)):
    new_currency = ExchangeCurrency(
        currency_name="Рубль",
        currency_symbol="RUB",
        currency_price=100.4
    )
    session.add(new_currency)
    await session.commit()
    return "OK"



@exchange_router.post("/convert")
async def convert(request: ConvertRequest):
    ...
