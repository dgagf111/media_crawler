"""
统一异常处理系统

定义项目中所有的自定义异常类，提供统一的异常处理机制。
"""

from typing import Optional, Dict, Any
from .constants import error_codes, messages

class BaseCustomException(Exception):
    """基础自定义异常类"""
    
    def __init__(
        self,
        code: int = error_codes.SYSTEM_ERROR,
        message: str = messages.SYSTEM_ERROR_MSG,
        detail: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.detail = detail or message
        self.data = data
        super().__init__(self.detail)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "code": self.code,
            "message": self.message,
            "detail": self.detail,
            "data": self.data
        }

# === 认证相关异常 ===
class AuthenticationException(BaseCustomException):
    """认证异常基类"""
    pass

class InvalidTokenException(AuthenticationException):
    """无效令牌异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.TOKEN_INVALID,
            message=messages.TOKEN_INVALID_MSG,
            detail=detail
        )

class TokenExpiredException(AuthenticationException):
    """令牌过期异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.TOKEN_EXPIRED,
            message=messages.TOKEN_EXPIRED_MSG,
            detail=detail
        )

class TokenRevokedException(AuthenticationException):
    """令牌被撤销异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.TOKEN_INVALID,
            message="Token has been revoked",
            detail=detail
        )

class InvalidCredentialsException(AuthenticationException):
    """无效凭据异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.UNAUTHORIZED,
            message="Invalid credentials",
            detail=detail
        )

class IncorrectCredentialsException(AuthenticationException):
    """凭据错误异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.PASSWORD_ERROR,
            message=messages.PASSWORD_ERROR_MSG,
            detail=detail
        )

# === 授权相关异常 ===
class PermissionDeniedException(BaseCustomException):
    """权限不足异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.PERMISSION_DENIED,
            message=messages.PERMISSION_DENIED_MSG,
            detail=detail
        )

# === 用户相关异常 ===
class UserException(BaseCustomException):
    """用户异常基类"""
    pass

class UserNotFoundException(UserException):
    """用户未找到异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.USER_NOT_FOUND,
            message=messages.USER_NOT_FOUND_MSG,
            detail=detail
        )

class UserAlreadyExistsException(UserException):
    """用户已存在异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.USER_ALREADY_EXISTS,
            message="User already exists",
            detail=detail
        )

class UserDisabledException(UserException):
    """用户已禁用异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.USER_DISABLED,
            message="User has been disabled",
            detail=detail
        )

# === 资源相关异常 ===
class ResourceException(BaseCustomException):
    """资源异常基类"""
    pass

class ResourceNotFoundException(ResourceException):
    """资源未找到异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.RESOURCE_NOT_FOUND,
            message="Resource not found",
            detail=detail
        )

class ResourceAlreadyExistsException(ResourceException):
    """资源已存在异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.RESOURCE_ALREADY_EXISTS,
            message="Resource already exists",
            detail=detail
        )

# === 验证相关异常 ===
class ValidationException(BaseCustomException):
    """验证异常"""
    
    def __init__(self, detail: str = None, data: Dict[str, Any] = None):
        super().__init__(
            code=error_codes.PARAMETER_ERROR,
            message=messages.PARAMETER_ERROR_MSG,
            detail=detail,
            data=data
        )

class InvalidParameterException(ValidationException):
    """无效参数异常"""
    pass

# === 业务逻辑异常 ===
class BusinessException(BaseCustomException):
    """业务逻辑异常"""
    
    def __init__(self, code: int, message: str, detail: str = None):
        super().__init__(code=code, message=message, detail=detail)

class OperationNotAllowedException(BusinessException):
    """操作不被允许异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.OPERATION_NOT_ALLOWED,
            message="Operation not allowed",
            detail=detail
        )

# === 系统异常 ===
class SystemException(BaseCustomException):
    """系统异常"""
    pass

class DatabaseException(SystemException):
    """数据库异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.SYSTEM_ERROR,
            message="Database error",
            detail=detail
        )

class CacheException(SystemException):
    """缓存异常"""
    
    def __init__(self, detail: str = None):
        super().__init__(
            code=error_codes.SYSTEM_ERROR,
            message="Cache error",
            detail=detail
        )

class ExternalServiceException(SystemException):
    """外部服务异常"""
    
    def __init__(self, service_name: str, detail: str = None):
        super().__init__(
            code=error_codes.SYSTEM_ERROR,
            message=f"External service '{service_name}' error",
            detail=detail
        )

# === API异常 (为了向后兼容) ===
APIException = BaseCustomException