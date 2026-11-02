from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    Фамилия: str = Field(min_length=1, max_length=100)
    Имя: str = Field(min_length=1, max_length=100)
    Пол: Literal["М", "Ж"]
    Возраст: int = Field(ge=18, le=100)
    Рост: int = Field(ge=100, le=250)
    Город: str = Field(min_length=1, max_length=100)
    Должность: str = Field(min_length=1, max_length=100)
    Зарплата: int = Field(gt=0)
    Транспорт: str | None = None
