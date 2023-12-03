from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import CommonResponse


class ConvertRequest(BaseModel):
    currency_from: str = Field(description="Первая валюта")
    currency_to: str = Field(description="Вторая валюта")
    currency_amount: float = Field(description="Количество")


class CurrencyLastUpdate(BaseModel):
    currency_symbol: str
    last_update: datetime


class LastUpdateResponse(CommonResponse):
    result: list


class ConvertResponse(CommonResponse):
    result: float | None
