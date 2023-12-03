from datetime import datetime

from celery import shared_task
from httpx import Client
from sqlalchemy import select

from app.utils.database_sync import Session
from app.models.exchange_models import ExchangeCurrency
from settings.config import ConfigExchangeApi

from celery import Celery
from celery.schedules import schedule

from settings.config import ConfigCelery
from settings.constants import WAIT_IN_SECONDS_PERIODIC_TASK

celery_app = Celery(
    'jobs',
    broker=ConfigCelery.BROKER,
    backend=ConfigCelery.BACKEND
)

celery_app.conf.beat_schedule = {
    "update-currency": {
        "task": "app.jobs.update_job.update_currency",
        "schedule": schedule(run_every=WAIT_IN_SECONDS_PERIODIC_TASK)
    }
}


@shared_task
def update_currency():
    """ Фоновая периодическая синхронная задача обновляющая курс"""

    # Инициализируем клиента и делаем запрос
    client = Client()
    response_get_price = client.get(
        f"{ConfigExchangeApi.PRICES_URL}{ConfigExchangeApi.API_KEY}")
    response_get_names = client.get(ConfigExchangeApi.NAMES_URL)
    prices = response_get_price.json()["rates"]
    names = response_get_names.json()

    # Открываем соединение с базой данных
    with Session() as session:
        # Проходимся по полученным валютам
        for symbol in prices:
            # Проверяем существует ли валюта в базе
            query = select(ExchangeCurrency).where(
                ExchangeCurrency.currency_symbol == symbol)
            result = session.execute(query)
            currency = result.scalars().first()

            if currency:
                # Если валюта существует мы ее обновляем
                try:
                    currency.currency_symbol = symbol
                    currency.currency_price = float(prices[symbol])
                    currency.currency_name = names.get(symbol, "Undefined"),
                    currency.updated_at=datetime.utcnow()
                except KeyError:
                    currency.currency_symbol = symbol
                    currency.currency_price = float(prices[symbol])
                    currency.currency_name = "Undefined",
                    currency.updated_at=datetime.utcnow()
            else:
                # Если нет - добавляем
                try:
                    new_currency = ExchangeCurrency(
                        currency_symbol=symbol,
                        currency_price=float(prices[symbol]),
                        currency_name=names.get(symbol, "Undefined"),
                        updated_at=datetime.utcnow()
                    )
                    session.add(new_currency)
                except KeyError:
                    new_currency = ExchangeCurrency(
                        currency_symbol=symbol,
                        currency_price=float(prices[symbol]),
                        currency_name="Undefined",
                        updated_at=datetime.utcnow()
                    )
                    session.add(new_currency)
        # Комитим изменения
        session.commit()
