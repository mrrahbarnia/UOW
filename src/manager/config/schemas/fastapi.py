from pydantic_settings import BaseSettings


class FastAPI(BaseSettings):
    ENDPOINT_PREFIX: str
    DOCS_URL: str
    REDOC_URL: str
    OPENAPI_URL: str
