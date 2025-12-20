from fastapi import APIRouter

from src.manager.config import ENVS
from src.app_book.entrypoints.v1 import router as book_router

router = APIRouter(prefix=f"{ENVS.FASTAPI.ENDPOINT_PREFIX}")

router.include_router(router=book_router.app)
