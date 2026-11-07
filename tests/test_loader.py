import json
from pathlib import Path
from typing import Any

import pytest

from hr_analytics.config import Settings
from hr_analytics.services.loader import load_data
from tests.test_filtering import BASE


class FakeSink:
    def __init__(self) -> None:
        self.docs: list[dict[str, Any]] = []

    def bulk_index(self, docs: list[dict[str, Any]]) -> int:
        self.docs = docs
        return len(docs)


def test_load_data_stats(tmp_path: Path) -> None:
    rows = [BASE, {**BASE, "Зарплата": 40_000}, {**BASE, "Фамилия": ""}]
    path = tmp_path / "job.json"
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    sink = FakeSink()
    stats = load_data(Settings(_env_file=None, data_path=path), sink)

    assert (stats.total, stats.invalid, stats.filtered, stats.indexed) == (3, 1, 1, 1)


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_data(Settings(_env_file=None, data_path=tmp_path / "nope.json"), FakeSink())