from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.exchange_schemas import ConvertRequest
from app.utils.database_async import get_session
from app.controllers.exchange_controllers import ExchangeControllers
from app.schemas.exchange_schemas import LastUpdateResponse, ConvertResponse

exchange_router = APIRouter(prefix="/exchange")


@exchange_router.get("/last_db_update")
async def get_last_db_update(session: AsyncSession = Depends(get_session)) -> LastUpdateResponse:
    response = await ExchangeControllers.get_last_updates(session)
    return LastUpdateResponse(result=response)


@exchange_router.post("/convert")
async def convert(request: ConvertRequest, session: AsyncSession = Depends(get_session)) -> ConvertResponse:
    response = await ExchangeControllers.convert(session, request.currency_to, request.currency_from, request.currency_amount)
    return response
