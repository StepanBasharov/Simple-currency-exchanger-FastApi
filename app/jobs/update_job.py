from celery import Celery
from celery.schedules import schedule
from httpx import AsyncClient

from app.utils.database import get_session
from app.models.exchange_models import ExchangeCurrency
from settings.config import ConfigCelery, ConfigExchangeApi


celery_app = Celery(
    'jobs',
    broker=ConfigCelery.BROKER,
    backend=ConfigCelery.BACKEND
)

celery_app.conf.beat_schedule =  {
    "run-periodic-task": {
        "task": "main.update_currency",
        "schedule": schedule(run_every=30)
    }
}

@celery_app.task
async def update_currency():
    async with AsyncClient() as client:
        response_get_price = await client.get(f"{ConfigExchangeApi.PRICES_URL}{ConfigExchangeApi.API_KEY}")
        response_get_names = await client.get(ConfigExchangeApi.NAMES_URL)
        prices = response_get_price.json()["rates"]
        names = response_get_names.json()
        for symbol in prices:
            try:
                async with get_session() as session:
                    currency = session.query(ExchangeCurrency).filter_by(symbol=symbol).first()
                    if currency:
                        currency.currency_symbol = symbol
                        currency.currency_price = float(prices[symbol])
                        currency.currency_name = names[symbol]
                        await session.commit()
                    else:
                        new_currency = ExchangeCurrency(
                            currency_symbol=symbol,
                            currency_price=float(prices[symbol]),
                            currency_name=names[symbol]
                        )
                        session.add(new_currency)
                        await session.commit()
            except KeyError:
                new_currency = ExchangeCurrency(
                    currency_symbol=symbol,
                    currency_price=float(prices[symbol]),
                    currency_name="Undefined"
                )
                session.add(new_currency)
                await session.commit()

