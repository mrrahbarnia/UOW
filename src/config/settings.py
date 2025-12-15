from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from . import schemas
from src.common.types import Environment


class _ENVS(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
    )
    ENVIRONMENT: Environment
    POSTGRESQL: schemas.PostgreSQL
    FASTAPI: schemas.FastAPI


@lru_cache
def get_envs() -> _ENVS:
    return _ENVS()  # type: ignore


ENVS = get_envs()
