import pytest

from hr_analytics.config import Settings
from hr_analytics.schemas import EmployeeIn
from hr_analytics.services.filtering import passes_rules

BASE = {
    "Фамилия": "Иванов",
    "Имя": "Иван",
    "Пол": "М",
    "Возраст": 30,
    "Рост": 175,
    "Город": "Москва",
    "Должность": "Аналитик",
    "Зарплата": 120_000,
}


@pytest.mark.parametrize(
    ("salary", "height", "expected"),
    [
        (50_000, 161, True),
        (200_000, 190, True),
        (49_999, 175, False),
        (200_001, 175, False),
        (120_000, 160, False),
    ],
)
def test_passes_rules(salary: int, height: int, expected: bool) -> None:
    emp = EmployeeIn(**{**BASE, "Зарплата": salary, "Рост": height})
    assert passes_rules(emp, Settings(_env_file=None)) is expected
