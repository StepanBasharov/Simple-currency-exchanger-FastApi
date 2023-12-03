from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exchange_models import ExchangeCurrency
from app.schemas.exchange_schemas import (
    CurrencyLastUpdate,
    ConvertResponse
)


class ExchangeControllers:
    @staticmethod
    async def get_last_updates(session: AsyncSession) -> List[CurrencyLastUpdate]:
        updates = []
        query = select(ExchangeCurrency)
        result = await session.execute(query)
        currency = result.scalars().all()
        for symbol in currency:
            updates.append(
                CurrencyLastUpdate(
                    currency_symbol=symbol.currency_symbol,
                    last_update=symbol.updated_at
                )
            )
        return updates

    @staticmethod
    async def convert(
            session: AsyncSession,
            currency_from: str,
            currency_to: str,
            amount: float
    ) -> ConvertResponse:
        query = select(ExchangeCurrency).where(
            ExchangeCurrency.currency_symbol == currency_from)
        result = await session.execute(query)
        currency_from_price = result.scalars().first()
        query = select(ExchangeCurrency).where(
            ExchangeCurrency.currency_symbol == currency_to)
        result = await session.execute(query)
        currency_to_price = result.scalars().first()
        result = currency_from_price.currency_price + \
            amount / currency_to_price.currency_price
        return ConvertResponse(result=result)
