from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Config(BaseSettings):
    database_url: str
    postgres_echo: bool | None = None

    class Config:
        env_file = BASE_DIR / ".env"


config = Config()
