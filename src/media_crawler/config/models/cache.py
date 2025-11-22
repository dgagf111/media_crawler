from __future__ import annotations

from pydantic import BaseModel


class CacheRedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0


class CacheSettings(BaseModel):
    type: str = "memory"
    ttl: int = 3600
    max_size: int = 1000
    redis: CacheRedisSettings = CacheRedisSettings()


__all__ = ["CacheSettings", "CacheRedisSettings"]
