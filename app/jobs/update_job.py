from celery import Celery, shared_task
from celery.schedules import schedule
from httpx import Client

from app.utils.database_async import get_session
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
        "schedule": schedule(run_every=10)
    }
}


@shared_task
def update_currency():
    print("ROOOOB")
    client = Client()
    response_get_price = client.get(f"{ConfigExchangeApi.PRICES_URL}{ConfigExchangeApi.API_KEY}")
    response_get_names = client.get(ConfigExchangeApi.NAMES_URL)
    prices = response_get_price.json()["rates"]
    names = response_get_names.json()

    currencies_to_add = []
    currencies_to_update = []

    for symbol in prices:
        with get_session() as session:
            currency = session.query(ExchangeCurrency).filter_by(symbol=symbol).first()
            if currency:
                try:
                    currency.currency_symbol = symbol
                    currency.currency_price = float(prices[symbol])
                    currency.currency_name = names[symbol]
                    currencies_to_update.append(currency)
                except KeyError:
                    currency.currency_symbol = symbol
                    currency.currency_price = float(prices[symbol])
                    currency.currency_name = "Undefined"
                    currencies_to_update.append(currency)
            else:
                try:
                    new_currency = ExchangeCurrency(
                        currency_symbol=symbol,
                        currency_price=float(prices[symbol]),
                        currency_name=names[symbol]
                    )
                    currencies_to_add.append(new_currency)
                except KeyError:
                    new_currency = ExchangeCurrency(
                        currency_symbol=symbol,
                        currency_price=float(prices[symbol]),
                        currency_name="Undefined"
                    )
                    currencies_to_add.append(new_currency)
    if currencies_to_update:
        session.bulk_save_objects(currencies_to_update)
    if currencies_to_add:
        session.bulk_save_objects(currencies_to_add)
