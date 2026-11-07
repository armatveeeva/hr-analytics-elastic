from hr_analytics.config import Settings
from hr_analytics.schemas import EmployeeIn


def passes_rules(emp: EmployeeIn, settings: Settings) -> bool:
    return bool(
        settings.salary_min <= emp.Зарплата <= settings.salary_max
        and emp.Рост > settings.height_min_exclusive
    )
