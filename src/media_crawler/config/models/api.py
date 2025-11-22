from __future__ import annotations

from pydantic import BaseModel, Field


class ApiSettings(BaseModel):
    title: str = "Python Project Template API"
    description: str = "A production ready FastAPI service"
    version: str = "3.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    loop: str = "asyncio"
    open_api_on_startup: bool = True
    docs_url: str | None = "/docs"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    max_concurrency: int = 100
    request_timeout: int = 30


__all__ = ["ApiSettings"]
