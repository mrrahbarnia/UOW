from typing import Any

from fastapi import HTTPException, status

from src.config import ENVS
from src.common.types import Environment


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
