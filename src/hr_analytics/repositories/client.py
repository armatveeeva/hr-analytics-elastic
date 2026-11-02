from elasticsearch import Elasticsearch

from hr_analytics.config import Settings


def build_client(settings: Settings) -> Elasticsearch:
    if settings.es_api_key:
        return Elasticsearch(
            settings.es_url,
            api_key=settings.es_api_key.get_secret_value(),
            verify_certs=settings.es_verify_certs,
            request_timeout=30,
        )
    if settings.es_user and settings.es_password:
        return Elasticsearch(
            settings.es_url,
            basic_auth=(settings.es_user, settings.es_password.get_secret_value()),
            verify_certs=settings.es_verify_certs,
            request_timeout=30,
        )
    return Elasticsearch(settings.es_url, verify_certs=settings.es_verify_certs, request_timeout=30)
