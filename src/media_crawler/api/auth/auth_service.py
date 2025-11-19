import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from typing import Optional, Dict, Any, Union, AsyncGenerator
from sqlalchemy import select

from pythonprojecttemplate.api.auth.token_service import create_tokens, verify_token
from pythonprojecttemplate.cache.cache_manager import get_cache_manager
from pythonprojecttemplate.db.session import AsyncSessionLocal, AsyncSession
from ..models.auth_models import User, Token
from .utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .token_types import TokenType
from pythonprojecttemplate.cache.cache_keys_manager import CacheKeysManager
from pythonprojecttemplate.api.exception.custom_exceptions import (
    InvalidTokenException,
    UserNotFoundException,
    InvalidCredentialsException,
    IncorrectCredentialsException,
    DatabaseException
)
from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger

logger = get_logger()

# 获取缓存键管理器
cache_keys = CacheKeysManager()

# 创建密码上下文，用于密码哈希和验证
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建OAuth2密码承载流程
API_TOKEN_PATH = f"/api/{settings.common.api_version}/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_TOKEN_PATH)

# 使用缓存管理器实例
cache_manager = get_cache_manager()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取异步数据库会话（FastAPI 依赖注入用）

    使用方式:
    async def endpoint(session: AsyncSession = Depends(get_db)):
        ...

    注意：不要手动调用此函数，应该通过 Depends(get_db) 使用
    """
    async with AsyncSessionLocal() as session:
        yield session

def generate_secret_key():
    """
    生成一个随机的密钥。
    用于为每个用户创建唯一的密钥。
    """
    return os.urandom(32).hex()

def save_secret_key(username: str, secret_key: str):
    """
    将用户的密钥保存到缓存中的secret_key大map结构。
    
    :param username: 用户名
    :param secret_key: 生成的密钥
    """
    secret_key_map = cache_manager.get(cache_keys.get_auth_secret_key_map_key()) or {}
    secret_key_map[username] = secret_key
    cache_manager.set(cache_keys.get_auth_secret_key_map_key(), secret_key_map, ttl=ACCESS_TOKEN_EXPIRE_MINUTES * 60)

def get_secret_key(username: str):
    """
    从缓存中的secret_key大map结构获取用户的密钥。
    
    :param username: 用户名
    :return: 用户的密钥，如果不存在则返回None
    """
    secret_key_map = cache_manager.get(cache_keys.get_auth_secret_key_map_key()) or {}
    return secret_key_map.get(username)

def verify_password(plain_password, hashed_password):
    """
    验证明文密码是否与哈希密码匹配。
    
    :param plain_password: 明文密码
    :param hashed_password: 哈希后的密码
    :return: 如果密码匹配返回True，否则返回False
    """
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(session: AsyncSession, username: str) -> Optional[User]:
    """
    根据用户名从数据库中获取用户。

    Args:
        session: 异步数据库会话
        username: 用户名

    Returns:
        用户对象，如果不存在则返回 None

    Raises:
        DatabaseException: 数据库查询失败
    """
    try:
        result = await session.execute(
            select(User).where(User.username == username, User.state >= 0)
        )
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"数据库查询用户失败: {e}", exc_info=True)
        raise DatabaseException(detail=f"查询用户失败: {str(e)}")

async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str
) -> Union[Dict[str, str], None]:
    """
    验证用户凭据

    Args:
        session: 异步数据库会话
        username: 用户名
        password: 密码（明文）

    Returns:
        成功: 包含 access_token 和 refresh_token 的字典
        失败: None

    Raises:
        IncorrectCredentialsException: 密码错误时抛出
    """
    user = await get_user(session, username)
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        raise IncorrectCredentialsException(detail="密码错误")

    access_token, refresh_token = create_tokens(user.username)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

def create_access_token(data: dict, username: str, expires_delta: Optional[timedelta] = None):
    """
    创建访问令牌并将其存储在token大map结构中。
    
    :param data: 要编码到令牌中的数据
    :param username: 用户名，用于获取用户特定的密钥
    :param expires_delta: 令牌的过期时间增量
    :return: 编码后的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.setdefault("type", TokenType.ACCESS.value)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # 将token存储在token大map结构中
    token_map = cache_manager.get(cache_keys.get_auth_token_map_key()) or {}
    token_map[username] = encoded_jwt
    cache_manager.set(cache_keys.get_auth_token_map_key(), token_map, ttl=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    """
    从JWT令牌中获取当前用户，并验证token是否存在于token大map结构中。

    :param token: JWT令牌
    :param session: 异步数据库会话
    :return: 当前用户对象
    :raises InvalidTokenException: 如果凭据无效
    :raises UserNotFoundException: 如果用户不存在
    """
    try:
        payload = verify_token(token)
        token_type = TokenType.from_payload(payload)
        if token_type != TokenType.ACCESS:
            raise InvalidTokenException(detail="Invalid token type")
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenException()

        user = await get_user(session, username)
        if user is None:
            raise UserNotFoundException()
        return user
    except JWTError:
        raise InvalidTokenException()

# 新增函数：创建新用户
async def create_user(session: AsyncSession, username: str, password: str, email: str):
    """创建新用户"""
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, password_hash=hashed_password, email=email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

# 新增函数：保存token
async def save_token(session: AsyncSession, user_id: int, token: str, token_type: int, expires_at: datetime):
    """保存token到数据库"""
    new_token = Token(user_id=user_id, token=token, token_type=token_type, expires_at=expires_at)
    session.add(new_token)
    await session.commit()
    await session.refresh(new_token)
    return new_token

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 新增函数：验证永久token
from .token_service import verify_permanent_token

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_provider_header = APIKeyHeader(name="X-API-Provider", auto_error=False)

async def get_current_app(
    api_key: str = Depends(api_key_header),
    provider: str = Depends(api_provider_header),
    session: AsyncSession = Depends(get_db),
):
    """验证API密钥"""
    if not api_key:
        raise InvalidCredentialsException(detail="API key is missing")
    if not provider:
        raise InvalidCredentialsException(detail="API provider is missing")
    if not await verify_permanent_token(session, api_key, provider):
        raise InvalidTokenException(detail="Invalid API key or provider")
    return provider
