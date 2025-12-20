from fastapi import status

from src.manager.application.exception_handler import AppBaseException


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
