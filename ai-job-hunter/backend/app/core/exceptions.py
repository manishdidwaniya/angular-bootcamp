"""自定义异常和全局异常处理器。"""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.config import settings


class AppException(Exception):
    """应用基础异常。"""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, resource: str, id: str | int):
        super().__init__(
            message=f"{resource} with id '{id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "id": str(id)},
        )


class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Access denied."):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationException(AppException):
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message=message, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, details=details
        )


class ExternalServiceException(AppException):
    def __init__(self, service: str, message: str = "External service error."):
        super().__init__(
            message=f"[{service}] {message}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details={"service": service},
        )


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局异常处理器。"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "details": exc.details,
                    "status": exc.status_code,
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": (
                        "An unexpected error occurred." if settings.is_production else str(exc)
                    ),
                    "details": {},
                    "status": 500,
                }
            },
        )
