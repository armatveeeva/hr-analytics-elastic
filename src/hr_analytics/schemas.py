from pydantic import BaseModel, Field


class EmployeeIn(BaseModel):
    Фамилия: str = Field(..., min_length=1)
    Имя: str = Field(..., min_length=1)
    Пол: str
    Возраст: int = Field(gt=18, lt=100)
    Рост: int = Field(gt=100, lt=250)
    Город: str
    Должность: str
    Зарплата: int = Field(gt=0)
    Транспорт: str | None = None