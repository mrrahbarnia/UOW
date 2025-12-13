from pydantic_settings import BaseSettings

from src.common.types import Environment


class General(BaseSettings):
    ENVIRONMENT: Environment
