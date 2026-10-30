import json
import logging
from pathlib import Path

from pydantic import ValidationError

from hr_analytics.config import Settings
from hr_analytics.repositories.employees import EmployeeRepository
from hr_analytics.schemas import EmployeeIn
from hr_analytics.services.filtering import passes_rules

log = logging.getLogger(__name__)


def load_data(data_path: str, settings: Settings, repo: EmployeeRepository) -> None:
    file_path = Path(data_path)
    if not file_path.exists():
        log.warning("Файл данных не найден: %s", data_path)
        return

    with file_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if not isinstance(raw_data, list):
        log.error("Ожидался список записей в исходном файле")
        return

    valid_docs = []
    invalid_count = 0
    filtered_count = 0

    for i, row in enumerate(raw_data):
        try:
            emp = EmployeeIn(**row)
        except ValidationError as exc:
            invalid_count += 1
            log.debug("Невалидная строка %d: %s", i, exc)
            continue

        if passes_rules(emp, settings):
            valid_docs.append(emp.model_dump())
        else:
            filtered_count += 1

    log.info(
        "Обработано записей: всего=%d, невалидных=%d, отфильтровано=%d, принято=%d",
        len(raw_data), invalid_count, filtered_count, len(valid_docs)
    )

    if valid_docs:
        repo.bulk_index(valid_docs)
    else:
        log.warning("Нет валидных записей для индексации после фильтрации.")