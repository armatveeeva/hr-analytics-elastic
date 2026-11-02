import pytest
from pydantic import ValidationError

from hr_analytics.schemas import EmployeeIn
from tests.test_filtering import BASE


def test_age_18_is_valid() -> None:
    assert EmployeeIn(**{**BASE, "Возраст": 18}).Возраст == 18


@pytest.mark.parametrize(
    "patch",
    [{"Возраст": 17}, {"Пол": "X"}, {"Фамилия": ""}, {"Зарплата": 0}],
)
def test_invalid_rows_rejected(patch: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        EmployeeIn(**{**BASE, **patch})
