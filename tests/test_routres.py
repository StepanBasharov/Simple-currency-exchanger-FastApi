import pytest
from httpx import Client

from app.schemas.exchange_schemas import ConvertRequest


from settings.config import ConfigService

BASE_URL = f"http://{ConfigService.HOST}:{ConfigService.PORT}"


def test_ping():
    with Client() as client:
        response = client.get(BASE_URL + "/api/service/ping")
        assert response.status_code == 200


def test_last_update():
    with Client() as client:
        response = client.get(BASE_URL + "/api/exchange/last_db_update")
        assert response.status_code == 200


def test_convert():
    with Client() as client:
        payload = ConvertRequest(
            currency_to="USD", currency_from="RUB", currency_amount=100.443).model_dump_json()
        response = client.post(
            BASE_URL + "/api/exchange/convert", content=payload)
        assert response.status_code == 200
        assert str(type(response.json()["result"])) == "<class 'float'>"
