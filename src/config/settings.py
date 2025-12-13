from functools import lru_cache

from pydantic import BaseModel

from . import schemas


class _ENVS(BaseModel):
    POSTGRESQL: schemas.PostgreSQL = schemas.PostgreSQL()  # type: ignore
    FASTAPI: schemas.FastAPI = schemas.FastAPI()  # type: ignore
    GENERAL: schemas.General = schemas.General()  # type: ignore


@lru_cache
def get_envs() -> _ENVS:
    return _ENVS()  # type: ignore


ENVS = get_envs()
