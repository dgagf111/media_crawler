from __future__ import annotations

from fastapi import HTTPException, status
from pythonprojecttemplate.api.http_status import HTTPStatus

class APIException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class InvalidCredentialsException(APIException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED.code, detail=detail)

class InvalidTokenException(APIException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED.code, detail=detail)

class TokenRevokedException(APIException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED.code, detail="Token has been revoked")

class UserNotFoundException(APIException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# 新增的异常类型
class IncorrectCredentialsException(APIException):
    def __init__(self, detail: str | None = None):
        message = detail or "Incorrect username or password"
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED.code, detail=message)

class InvalidTokenTypeException(APIException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED.code, detail="Invalid token type")

class RefreshTokenException(APIException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED.code, detail="Invalid or expired refresh token")

class DatabaseException(APIException):
    """数据库异常"""
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
