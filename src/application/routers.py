from fastapi import APIRouter

from src.config import ENVS
from src.modules.book.entrypoints.v1 import router as book_router

router = APIRouter(prefix=f"{ENVS.FASTAPI.ENDPOINT_PREFIX}")

router.include_router(router=book_router.app)
