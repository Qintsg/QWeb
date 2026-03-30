"""统一业务异常定义。

所有业务层异常应继承 BusinessException，在 exception_handler 中统一捕获并格式化输出。
"""

from __future__ import annotations

from rest_framework import status as http_status


class BusinessException(Exception):
    """通用业务异常基类。

    Attributes:
        message: 用户可读的错误描述。
        code: 业务错误码（非零）。
        status_code: 对应的 HTTP 状态码。
    """

    def __init__(
        self,
        message: str = "业务处理异常",
        code: int = 1,
        status_code: int = http_status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class PermissionDeniedException(BusinessException):
    """权限不足异常，默认返回 403。"""

    def __init__(
        self,
        message: str = "权限不足，拒绝访问",
        code: int = 4030,
    ) -> None:
        super().__init__(message=message, code=code, status_code=http_status.HTTP_403_FORBIDDEN)


class AuthenticationFailedException(BusinessException):
    """认证失败异常，默认返回 401。"""

    def __init__(
        self,
        message: str = "认证失败，请重新登录",
        code: int = 4010,
    ) -> None:
        super().__init__(message=message, code=code, status_code=http_status.HTTP_401_UNAUTHORIZED)


class ResourceNotFoundException(BusinessException):
    """资源不存在异常，默认返回 404。"""

    def __init__(
        self,
        message: str = "请求的资源不存在",
        code: int = 4040,
    ) -> None:
        super().__init__(message=message, code=code, status_code=http_status.HTTP_404_NOT_FOUND)


class ValidationException(BusinessException):
    """参数校验异常，默认返回 422。"""

    def __init__(
        self,
        message: str = "参数校验失败",
        code: int = 4220,
        errors: dict | list | None = None,
    ) -> None:
        self.errors = errors
        super().__init__(
            message=message,
            code=code,
            status_code=422,
        )


class ConflictException(BusinessException):
    """资源冲突异常，默认返回 409。"""

    def __init__(
        self,
        message: str = "资源已存在或状态冲突",
        code: int = 4090,
    ) -> None:
        super().__init__(message=message, code=code, status_code=http_status.HTTP_409_CONFLICT)
