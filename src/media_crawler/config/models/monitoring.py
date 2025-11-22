from __future__ import annotations

from pydantic import BaseModel, Field


class MonitoringSettings(BaseModel):
    prometheus_port: int = 9966
    cpu_threshold: int = 80
    memory_threshold: int = 80
    interval_seconds: int = Field(default=60, ge=5, le=3600)
    max_retries: int = Field(default=3, ge=0, le=50)
    retry_interval_seconds: int = Field(default=5, ge=1, le=300)


__all__ = ["MonitoringSettings"]
