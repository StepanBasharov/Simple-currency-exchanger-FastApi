from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class CommonResponse(BaseModel):
    code: int = Field(description="Код ответа", default=200)
    status: str = Field(description="Статус ответа", default="success")
    time: datetime = Field(description="Время ответа")
