from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    currency_from: str = Field(description="Первая валюта")
    currency_to: str = Field(description="Вторая валюта")
    currency_amount: float = Field(description="Количество")
