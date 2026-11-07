import json
import logging
from dataclasses import dataclass
from typing import Any, Protocol

from hr_analytics.config import Settings
from hr_analytics.schemas import EmployeeIn
from hr_analytics.services.filtering import passes_rules
from pydantic import ValidationError

log = logging.getLogger(__name__)


class DocumentSink(Protocol):
    def bulk_index(self, docs: list[dict[str, Any]]) -> int: ...


@dataclass(frozen=True)
class LoadStats:
    total: int
    invalid: int
    filtered: int
    indexed: int


def load_data(settings: Settings, sink: DocumentSink) -> LoadStats:
    data_path = settings.data_path
    if not data_path.exists():
        raise FileNotFoundError(f"Файл данных не найден: {data_path}")

    raw_data: list[Any] = json.loads(data_path.read_text(encoding="utf-8"))
    if not isinstance(raw_data, list):
        raise ValueError("Ожидался список записей в исходном файле")

    docs: list[dict[str, Any]] = []
    invalid = filtered = 0
    for i, row in enumerate(raw_data):
        try:
            emp = EmployeeIn.model_validate(row)
        except ValidationError as exc:
            invalid += 1
            log.warning("Невалидная строка %d: %s", i, exc.errors(include_url=False))
            continue
        if passes_rules(emp, settings):
            docs.append(emp.model_dump())
        else:
            filtered += 1

    indexed = sink.bulk_index(docs) if docs else 0
    if not docs:
        log.warning("Нет записей для индексации после валидации и фильтрации")
        return LoadStats(len(raw_data), invalid, filtered, 0)

    indexed = sink.bulk_index(docs)
    return LoadStats(len(raw_data), invalid, filtered, indexed)
