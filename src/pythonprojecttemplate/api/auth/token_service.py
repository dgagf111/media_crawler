from __future__ import annotations

from datetime import UTC, datetime, timedelta
import secrets
from typing import Tuple
from zoneinfo import ZoneInfo

from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pythonprojecttemplate.api.auth.token_registry import (
    TokenRecord,
    token_audit_logger,
    token_registry,
)
from pythonprojecttemplate.api.auth.token_types import TokenType
from pythonprojecttemplate.api.exception.custom_exceptions import (
    InvalidTokenException,
    TokenRevokedException,
)
from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger
from ..models.auth_models import ThirdPartyToken
from .utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
)

logger = get_logger()

TIME_ZONE = ZoneInfo(settings.common.time_zone)
REFRESH_TOKEN_EXPIRE_DAYS = settings.security.token.refresh_token_expire_days


def _mint_token_record(username: str) -> tuple[TokenRecord, str, str]:
    issued_at = datetime.now(UTC)
    access_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token({}, username=username, expires_delta=access_delta)
    refresh_token = create_refresh_token({}, username=username, expires_delta=refresh_delta)

    record = TokenRecord(
        username=username,
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires_at=issued_at + access_delta,
        refresh_expires_at=issued_at + refresh_delta,
        issued_at=issued_at,
    )
    return record, access_token, refresh_token


def create_tokens(username: str) -> Tuple[str, str]:
    record, access_token, refresh_token = _mint_token_record(username)
    token_registry.persist(record)
    token_audit_logger.log(
        "issued",
        username,
        access_expires_at=record.access_expires_at.isoformat(),
        refresh_expires_at=record.refresh_expires_at.isoformat(),
    )
    return access_token, refresh_token


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenException()
        if token_registry.is_token_revoked(token):
            raise TokenRevokedException()

        record = token_registry.read(username)
        if record is None:
            raise TokenRevokedException()

        token_type = TokenType.from_payload(payload)
        expected_token = (
            record.access_token if token_type == TokenType.ACCESS else record.refresh_token
        )
        if expected_token != token:
            raise TokenRevokedException()
        return payload
    except jwt.JWTError:
        raise InvalidTokenException()


def refresh_access_token(refresh_token: str) -> Tuple[str, str]:
    payload = verify_token(refresh_token)
    token_type = TokenType.from_payload(payload)
    if token_type != TokenType.REFRESH:
        raise InvalidTokenException(detail="Invalid token type")

    username = payload.get("sub")
    if not username:
        raise InvalidTokenException()

    record, access_token, new_refresh_token = _mint_token_record(username)
    token_registry.persist(record)
    token_audit_logger.log(
        "refreshed",
        username,
        access_expires_at=record.access_expires_at.isoformat(),
        refresh_expires_at=record.refresh_expires_at.isoformat(),
    )
    return access_token, new_refresh_token


def revoke_tokens(username: str) -> None:
    token_registry.revoke_user(username)
    token_audit_logger.log("revoked", username)


async def generate_permanent_token(session: AsyncSession, user_id: int, provider: str) -> str:
    """生成永久token并保存到数据库"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(TIME_ZONE) + timedelta(days=365 * 1000)
    new_token = ThirdPartyToken(
        user_id=user_id,
        provider=provider,
        third_party_token=token,
        expires_at=expires_at,
        state=0,
    )
    session.add(new_token)
    await session.commit()
    return token


async def verify_permanent_token(session: AsyncSession, token: str, provider: str) -> bool:
    """验证永久token"""
    try:
        result = await session.execute(
            select(ThirdPartyToken).where(
                ThirdPartyToken.third_party_token == token,
                ThirdPartyToken.provider == provider,
                ThirdPartyToken.state == 0,
            )
        )
        stored_token = result.scalar_one_or_none()

        if not stored_token:
            logger.debug(
                "Token not found for provider %s: %s...",
                provider,
                token[:10],
            )
            return False

        expires_at = stored_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=TIME_ZONE)

        is_valid = expires_at > datetime.now(TIME_ZONE)

        if not is_valid:
            logger.warning(
                "Token expired for provider %s: %s..., expires_at: %s",
                provider,
                token[:10],
                expires_at,
            )

        return is_valid

    except Exception as e:
        logger.error(f"验证token时发生错误: {e}", exc_info=True)
        return False
