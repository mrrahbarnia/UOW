from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
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
        if (ENVS.ENVIRONMENT == Environment.PRODUCTION) and (status_code >= 500):
            self.data = None
        else:
            self.data = str(data)

        self.message = message
        self.status_code = status_code
        self.success = success
        super().__init__(status_code=status_code)


# ========================== HTTP exceptions


class ServerError(AppBaseException):
    def __init__(self, data: str, message: str = "Server error."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            data=data,
        )


class BadRequestException(AppBaseException):
    def __init__(self, data: dict, message: str = "Bad request."):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            success=False,
            data=data,
        )


class EntityNotFoundException(AppBaseException):
    def __init__(self, data: dict, message: str = "Entity not found."):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            success=False,
            data=data,
        )


class DuplicateEntityException(AppBaseException):
    def __init__(self, data: dict, message: str = "Duplicate entity."):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            success=False,
            data=data,
        )


class ForbiddenException(AppBaseException):
    def __init__(self, data: dict | None = None, message: str = "Forbidden exception."):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            success=False,
            data=data,
        )
