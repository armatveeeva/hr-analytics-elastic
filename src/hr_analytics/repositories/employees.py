import json
import logging
from pathlib import Path
from typing import Any

from elasticsearch import Elasticsearch, helpers

log = logging.getLogger(__name__)


class EmployeeRepository:
    def __init__(self, client: Elasticsearch, index: str) -> None:
        self.client = client
        self.index = index

    def ensure_index(self, mapping_path: Path) -> None:
        if self.client.indices.exists(index=self.index):
            log.info("Индекс '%s' уже существует", self.index)
            return
        body = json.loads(mapping_path.read_text(encoding="utf-8"))
        self.client.indices.create(index=self.index, **body)
        log.info("Индекс '%s' создан", self.index)

    def bulk_index(self, docs: list[dict[str, Any]]) -> int:
        actions = ({"_index": self.index, "_source": d} for d in docs)
        ok, failed = helpers.bulk(self.client, actions, raise_on_error=False, stats_only=True)
        log.info("Проиндексировано документов: %d", ok)
        if failed:
            raise RuntimeError(f"Bulk-загрузка завершилась с ошибками: {failed}")
        return ok
