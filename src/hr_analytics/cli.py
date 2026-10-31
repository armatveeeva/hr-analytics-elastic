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
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="HR Analytics Elasticsearch Pipeline")
    parser.add_argument(
        "command",
        choices=["create-index", "load"],
        help="Команда для выполнения: create-index или load",
    )
    args = parser.parse_args()

    settings = Settings()
    setup_logging(settings.log_level)

    # === КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: Поддержка API Key ===
    if settings.es_api_key:
        logging.info("Подключение к Elasticsearch с использованием API Key...")
        es = Elasticsearch(
            settings.es_url,
            api_key=settings.es_api_key.get_secret_value(),
            verify_certs=False,
            request_timeout=30,
        )
    else:
        logging.info("Подключение к Elasticsearch с использованием Basic Auth...")
        es = Elasticsearch(
            settings.es_url,
            basic_auth=(settings.es_user, settings.es_password.get_secret_value()),
            verify_certs=False,
            request_timeout=30,
        )

    try:
        info = es.info()
        logging.info("Успешно подключено к Elasticsearch: %s", info["version"]["number"])
    except Exception as e:
        logging.error("Ошибка подключения к Elasticsearch: %s", e)
        return

    repo = EmployeeRepository(client=es, index=settings.index_name)

    if args.command == "create-index":
        logging.info("Выполняется создание индекса...")
        repo.ensure_index(settings.mapping_path)
        logging.info("Готово!")

    elif args.command == "load":
        logging.info("Запуск процесса загрузки данных...")
        load_data(settings.data_path, settings, repo)
        logging.info("Пайплайн успешно завершен.")


if __name__ == "__main__":
    main()
