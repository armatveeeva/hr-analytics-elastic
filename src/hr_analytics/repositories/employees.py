import json
import logging
from pathlib import Path

from elasticsearch import Elasticsearch, helpers

log = logging.getLogger(__name__)


class EmployeeRepository:
    def __init__(self, client: Elasticsearch, index: str) -> None:
        self.client = client
        self.index = index

    def ensure_index(self, mapping_path: str) -> None:
        if self.client.indices.exists(index=self.index):
            log.info("Индекс '%s' уже существует", self.index)
            return

        body = json.loads(Path(mapping_path).read_text(encoding="utf-8"))
        self.client.indices.create(index=self.index, **body)
        log.info("Индекс '%s' успешно создан", self.index)

    def bulk_index(self, docs: list[dict]) -> int:
        actions = ({"_index": self.index, "_source": d} for d in docs)
        ok, errors = helpers.bulk(self.client, actions, raise_on_error=False)
        if errors:
            log.error("Bulk-загрузка завершена с %d ошибками", len(errors))
        log.info("Успешно проиндексировано %d документов", ok)
        return ok