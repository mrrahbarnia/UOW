from fastapi import FastAPI

from src.manager.config import ENVS
from src.manager.common.types import Environment


app: FastAPI = FastAPI(
    title=ENVS.FASTAPI.APPLICATION_NAME,
    description=ENVS.FASTAPI.APPLICATION_DESCRIPTION,
    version=ENVS.FASTAPI.APPLICATION_VERSION,
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
