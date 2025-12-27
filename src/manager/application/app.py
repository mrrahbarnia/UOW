from fastapi import FastAPI

from src.manager.config import ENVS
from src.manager.common.types import Environment


app: FastAPI = FastAPI(
    title="book-borrow",
    description="People can borrow book in this application",
    version="0.0.1",
    docs_url=None
    if ENVS.ENVIRONMENT == Environment.PRODUCTION
    else ENVS.FASTAPI.DOCS_URL,
    openapi_url=None
    if ENVS.ENVIRONMENT == Environment.PRODUCTION
    else ENVS.FASTAPI.OPENAPI_URL,
    redoc_url=None
    if ENVS.ENVIRONMENT == Environment.PRODUCTION
    else ENVS.FASTAPI.REDOC_URL,
)
