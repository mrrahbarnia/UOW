from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPI(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FASTAPI__")

    APPLICATION_NAME: str
    APPLICATION_DESCRIPTION: str
    APPLICATION_VERSION: str
    ENDPOINT_PREFIX: str
    DOCS_URL: str
    REDOC_URL: str
    OPENAPI_URL: str
