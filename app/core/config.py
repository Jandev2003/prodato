import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    ENV: Literal["prod", "dev", "test"] = "dev"
    DEBUG: bool = False
    DATABASE_URL: (
        PostgresDsn  # verifica que la URL sea una conexión válida para PostgreSQL
    )
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR
        / f".env.{os.getenv('APP_ENV', 'dev')}",  # el último tiene prioridad
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="APP_",  # APP_DATABASE_URL, APP_DEBUG, ...
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
