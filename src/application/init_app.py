from fastapi import FastAPI

from src.application.app import app as fastapi_app
from src.application.exceptions import register_exception_handlers
from src.application.routers import router


def init_app(app: FastAPI) -> FastAPI:
    app.include_router(router)
    register_exception_handlers(app)
    return app


application: FastAPI = init_app(
    app=fastapi_app
)  # pass this to __main__.py or uvicorn command
