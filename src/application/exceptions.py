from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.config import ENVS
from src.common.types import Environment

# ========================== Custom exception handler


async def app_base_exception_handler(request: Request, exc: "AppBaseException"):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": exc.success,
            "status_code": exc.status_code,
            "message": exc.message,
            "data": exc.data,
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, app_base_exception_handler)  # type: ignore


class AppBaseException(HTTPException):
    def __init__(
        self,
        *,
        message: str,
        success: bool,
        status_code: int,
        data: Any | None = None,
    ):
        if (ENVS.GENERAL.ENVIRONMENT == Environment.PRODUCTION) and (
            status_code >= 500
        ):
            self.data = None
        else:
            self.data = str(data)

        self.message = message
        self.status_code = status_code
        self.success = success
        super().__init__(status_code=status_code)


# ========================== HTTP exceptions
