from typing import List, Optional

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
        # Получаем все валюты из бд
        query = select(ExchangeCurrency)
        result = await session.execute(query)
        currency = result.scalars().all()
        # Проходимя по валютам добавляя в список хеш-мапу
        # состоящую из кода валюты и даты ее обновления
        for symbol in currency:
            updates.append(
                CurrencyLastUpdate(
                    currency_symbol=symbol.currency_symbol,
                    last_update=symbol.updated_at
                )
            )
        # Возвращаем лист
        return updates

    @staticmethod
    async def convert(
            session: AsyncSession,
            currency_from: str,
            currency_to: str,
            amount: float
    ) -> Optional[ConvertResponse, None]:
        # Находим в базе первую и вторую валюты
        query = select(ExchangeCurrency).where(
            ExchangeCurrency.currency_symbol == currency_from)
        result = await session.execute(query)
        currency_from_price = result.scalars().first()
        query = select(ExchangeCurrency).where(
            ExchangeCurrency.currency_symbol == currency_to)
        result = await session.execute(query)
        currency_to_price = result.scalars().first()
        # По формуле вычисляем цену (from + amount / to)
        if currency_to_price.currency_price and currency_from_price.currency_price:
            result = currency_from_price.currency_price + \
                amount / currency_to_price.currency_price
            # Возвращаем результат
            return ConvertResponse(result=result)
        else:
            return None

