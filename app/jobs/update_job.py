import asyncio

from celery import Celery, shared_task
from celery.schedules import schedule
from httpx import Client
from sqlalchemy import select

from app.utils.database_sync import Session
from app.models.exchange_models import ExchangeCurrency
from settings.config import ConfigCelery, ConfigExchangeApi


celery_app = Celery(
    'jobs',
    broker=ConfigCelery.BROKER,
    backend=ConfigCelery.BACKEND
)

celery_app.conf.beat_schedule = {
    "run-periodic-task": {
        "task": "app.jobs.update_job.update_currency",
        "schedule": schedule(run_every=5)
    }
}


@shared_task
def update_currency():
    client = Client()
    response_get_price = client.get(
        f"{ConfigExchangeApi.PRICES_URL}{ConfigExchangeApi.API_KEY}")
    response_get_names = client.get(ConfigExchangeApi.NAMES_URL)
    prices = response_get_price.json()["rates"]
    names = response_get_names.json()

    with Session() as session:
        for symbol in prices:
            query = select(ExchangeCurrency).where(
                ExchangeCurrency.currency_symbol == symbol)
            result = session.execute(query)
            currency = result.scalars().first()

            if currency:
                try:
                    currency.currency_symbol = symbol
                    currency.currency_price = float(prices[symbol])
                    currency.currency_name = names.get(symbol, "Undefined")
                except KeyError:
                    currency.currency_symbol = symbol
                    currency.currency_price = float(prices[symbol])
                    currency.currency_name = "Undefined"
            else:
                try:
                    new_currency = ExchangeCurrency(
                        currency_symbol=symbol,
                        currency_price=float(prices[symbol]),
                        currency_name=names.get(symbol, "Undefined")
                    )
                    session.add(new_currency)
                except KeyError:
                    new_currency = ExchangeCurrency(
                        currency_symbol=symbol,
                        currency_price=float(prices[symbol]),
                        currency_name="Undefined"
                    )
                    session.add(new_currency)
        session.commit()
        print("Done")
