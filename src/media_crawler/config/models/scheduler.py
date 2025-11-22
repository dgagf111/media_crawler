from __future__ import annotations

from pydantic import BaseModel


class SchedulerExecutorsSettings(BaseModel):
    default_threads: int = 20
    process_pool: int = 5


class SchedulerJobDefaultsSettings(BaseModel):
    coalesce: bool = False
    max_instances: int = 3


class SchedulerSettings(BaseModel):
    executors: SchedulerExecutorsSettings = SchedulerExecutorsSettings()
    job_defaults: SchedulerJobDefaultsSettings = SchedulerJobDefaultsSettings()


__all__ = [
    "SchedulerExecutorsSettings",
    "SchedulerJobDefaultsSettings",
    "SchedulerSettings",
]
