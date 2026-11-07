import argparse
import logging
import sys

from hr_analytics.config import Settings
from hr_analytics.repositories.client import build_client
from hr_analytics.repositories.employees import EmployeeRepository
from hr_analytics.services.loader import load_data

log = logging.getLogger(__name__)


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HR Analytics Elasticsearch Pipeline")
    parser.add_argument("command", choices=["create-index", "load"])
    args = parser.parse_args(argv)

    settings = Settings()
    setup_logging(settings.log_level)

    client = build_client(settings)
    try:
        log.info("Elasticsearch %s", client.info()["version"]["number"])
    except Exception:
        log.exception("Не удалось подключиться к Elasticsearch (%s)", settings.es_url)
        return 1

    repo = EmployeeRepository(client=client, index=settings.index_name)
    try:
        if args.command == "create-index":
            repo.ensure_index(settings.mapping_path)
        else:
            stats = load_data(settings, repo)
            log.info(
                "Всего=%d, невалидных=%d, отфильтровано=%d, проиндексировано=%d",
                stats.total,
                stats.invalid,
                stats.filtered,
                stats.indexed,
            )
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        log.error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
