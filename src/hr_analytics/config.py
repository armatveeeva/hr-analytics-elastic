from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="HR_")

    es_url: str = "https://my-elasticsearch-project-d38065.es.us-east4.gcp.elastic.cloud:443"
    es_user: str = "elastic"
    es_password: SecretStr = SecretStr("changeme")
    es_api_key: SecretStr | None = None

    index_name: str = "workers_matveeva"
    mapping_path: str = "config/index_mapping.json"
    data_path: str = "data/job.json"

    salary_min: int = 50_000
    salary_max: int = 200_000
    height_min_exclusive: int = 160
    log_level: str = "INFO"
