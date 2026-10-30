import argparse
import logging

from elasticsearch import Elasticsearch

from hr_analytics.config import Settings
from hr_analytics.repositories.employees import EmployeeRepository
from hr_analytics.services.loader import load_data


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="HR Analytics Elasticsearch Pipeline")
    parser.add_argument("command", choices=["create-index", "load"], help="Команда для выполнения")
    args = parser.parse_args()

    settings = Settings()
    setup_logging(settings.log_level)

    es = Elasticsearch(
        settings.es_url,
        basic_auth=(settings.es_user, settings.es_password.get_secret_value()),
        verify_certs=False,
        request_timeout=30
    )

    try:
        es.info()
        logging.info("Подключено к Elasticsearch: %s", settings.es_url)
    except Exception as e:
        logging.error("Ошибка подключения к Elasticsearch: %s", e)
        return

    repo = EmployeeRepository(client=es, index=settings.index_name)

    if args.command == "create-index":
        repo.ensure_index(settings.mapping_path)
    elif args.command == "load":
        load_data(settings.data_path, settings, repo)