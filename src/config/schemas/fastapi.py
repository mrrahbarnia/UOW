from pydantic_settings import BaseSettings


class FastAPI(BaseSettings):
    APPLICATION_NAME: str
    APPLICATION_DESCRIPTION: str
    APPLICATION_VERSION: str
    ENDPOINT_PREFIX: str
    DOCS_URL: str
    REDOC_URL: str
    OPENAPI_URL: str
