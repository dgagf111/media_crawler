"""
核心工具函数

提供统一的工具函数，减少重复代码。
"""

from typing import Optional, Dict, Any, Union, AsyncGenerator
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from .constants import constants, cache_keys, error_codes, messages
from pythonprojecttemplate.api.auth.token_types import TokenType
from .logging.logger import get_logger
from .exceptions import InvalidTokenException, TokenRevokedException

logger = get_logger()

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTUtils:
    """JWT工具类"""
    
    @staticmethod
    def create_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        创建JWT令牌
        
        Args:
            data: 要编码的数据
            expires_delta: 过期时间增量
            
        Returns:
            编码后的JWT令牌
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, constants.JWT_SECRET_KEY, algorithm=constants.JWT_ALGORITHM)
        
        logger.debug(f"Created JWT token for data: {data}")
        return encoded_jwt
    
    @staticmethod
    def create_access_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建访问令牌
        
        Args:
            username: 用户名
            expires_delta: 过期时间增量
            
        Returns:
            访问令牌
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        data = {"sub": username, "type": TokenType.ACCESS.value}
        return JWTUtils.create_token(data, expires_delta)
    
    @staticmethod
    def create_refresh_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建刷新令牌
        
        Args:
            username: 用户名
            expires_delta: 过期时间增量
            
        Returns:
            刷新令牌
        """
        if expires_delta is None:
            expires_delta = timedelta(days=constants.REFRESH_TOKEN_EXPIRE_DAYS)
        
        data = {"sub": username, "type": TokenType.REFRESH.value}
        return JWTUtils.create_token(data, expires_delta)
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        验证JWT令牌
        
        Args:
            token: JWT令牌
            
        Returns:
            解码后的数据
            
        Raises:
            InvalidTokenException: 令牌无效或过期
        """
        try:
            payload = jwt.decode(token, constants.JWT_SECRET_KEY, algorithms=[constants.JWT_ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Invalid JWT token: {e}")
            raise InvalidTokenException(detail="Invalid or expired token")

class PasswordUtils:
    """密码工具类"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        对密码进行哈希加密
        
        Args:
            password: 原始密码
            
        Returns:
            哈希后的密码
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            plain_password: 原始密码
            hashed_password: 哈希密码
            
        Returns:
            验证结果
        """
        return pwd_context.verify(plain_password, hashed_password)

class DatabaseUtils:
    """数据库工具类"""
    
    @staticmethod
    async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
        """
        获取数据库会话
        
        这是一个异步生成器函数，用于依赖注入
        """
        try:
            from pythonprojecttemplate.db.session import AsyncSessionLocal
        except ImportError:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
            from pythonprojecttemplate.db.session import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception as e:
                logger.error("Database session error: %s", e, exc_info=True)
                await session.rollback()
                raise

class CacheUtils:
    """缓存工具类"""
    
    @staticmethod
    def get_cache_manager():
        """获取缓存管理器实例"""
        try:
            # 先尝试从新结构导入
            from ...core.cache.cache_manager import get_cache_manager
        except ImportError:
            try:
                # 再尝试从原结构导入
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
                from pythonprojecttemplate.cache.cache_manager import get_cache_manager
            except ImportError:
                logger.error("无法导入缓存管理器")
                return None
        return get_cache_manager()

class ResponseUtils:
    """响应工具类"""
    
    @staticmethod
    def success_response(data: Any = None, message: str = None) -> Dict[str, Any]:
        """
        成功响应
        
        Args:
            data: 响应数据
            message: 响应消息
            
        Returns:
            响应字典
        """
        return {
            "code": error_codes.SUCCESS,
            "message": message or messages.SUCCESS_MSG,
            "data": data
        }
    
    @staticmethod
    def error_response(code: int, message: str, data: Any = None) -> Dict[str, Any]:
        """
        错误响应
        
        Args:
            code: 错误代码
            message: 错误消息
            data: 响应数据
            
        Returns:
            响应字典
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }

class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号格式"""
        import re
        pattern = r'^1[3-9]\d{9}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        验证密码强度
        至少8位，包含大小写字母、数字和特殊字符
        """
        import re
        if len(password) < 8:
            return False
        
        patterns = [
            r'[a-z]',  # 小写字母
            r'[A-Z]',  # 大写字母  
            r'\d',     # 数字
            r'[!@#$%^&*(),.?":{}|<>]'  # 特殊字符
        ]
        
        return all(re.search(pattern, password) for pattern in patterns)

# 导出工具类实例
jwt_utils = JWTUtils()
password_utils = PasswordUtils()
database_utils = DatabaseUtils()
cache_utils = CacheUtils()
response_utils = ResponseUtils()
validation_utils = ValidationUtils()
