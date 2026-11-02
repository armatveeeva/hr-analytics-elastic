from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="HR_")

    es_url: str = "http://localhost:9200"
    es_user: str | None = None
    es_password: SecretStr | None = None
    es_api_key: SecretStr | None = None
    es_verify_certs: bool = True

    index_name: str = "workers_matveeva"
    mapping_path: Path = Path("config/index_mapping.json")
    data_path: Path = Path("data/job.json")

    salary_min: int = 50_000
    salary_max: int = 200_000
    height_min_exclusive: int = 160
    log_level: str = "INFO"
