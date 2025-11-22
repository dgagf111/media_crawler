from __future__ import annotations

import logging
from typing import Any, Literal

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator

logger = logging.getLogger(__name__)


class SecurityTokenSettings(BaseModel):
    secret_key: str = Field(default="change-me", min_length=8)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=180, ge=5, le=1440)
    refresh_token_expire_days: int = Field(default=7, ge=1, le=90)


class SecurityRedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 2
    username: str | None = None
    password: str | None = None
    ssl: bool = False

    @field_validator("host", mode="before")
    @classmethod
    def _ensure_host(cls, value: str | None) -> str:
        if value is None:
            return "localhost"
        host = value.strip()
        if not host:
            logger.warning("Empty Redis host detected, falling back to 'localhost'")
            return "localhost"
        return host

    @field_validator("port", "db", mode="before")
    @classmethod
    def _ensure_numeric(cls, value: Any, info: FieldValidationInfo) -> Any:
        if value in (None, "", " "):
            defaults = {"port": 6379, "db": 2}
            return defaults[info.field_name]
        return value


class SecurityRevocationSettings(BaseModel):
    backend: Literal["redis", "memory"] = "memory"
    redis: SecurityRedisSettings = SecurityRedisSettings()
    key_prefix: str = "ppt:security"
    default_ttl_seconds: int = Field(default=7 * 24 * 3600, gt=0)
    memory_cleanup_interval_seconds: int = Field(default=120, ge=5, le=3600)

    @field_validator("backend", mode="before")
    @classmethod
    def _normalize_backend(cls, value: str | None) -> str:
        if value is None:
            return "memory"
        backend = str(value).lower().strip()
        if backend not in {"redis", "memory"}:
            logger.warning("Unknown token backend '%s', using in-memory backend", value)
            return "memory"
        return backend


class TokenAuditSettings(BaseModel):
    enabled: bool = True
    include_username: bool = True


class SecuritySettings(BaseModel):
    token: SecurityTokenSettings = SecurityTokenSettings()
    revocation: SecurityRevocationSettings = SecurityRevocationSettings()
    audit: TokenAuditSettings = TokenAuditSettings()


__all__ = [
    "SecurityTokenSettings",
    "SecurityRedisSettings",
    "SecurityRevocationSettings",
    "SecuritySettings",
    "TokenAuditSettings",
]
