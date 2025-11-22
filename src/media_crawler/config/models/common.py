from __future__ import annotations

from pydantic import BaseModel


class ModuleSettings(BaseModel):
    base_path: str = "pythonprojecttemplate.modules"
    modules: list[str] = []


class LoggingSettings(BaseModel):
    project_name: str = "python_project_template"
    base_log_directory: str = "../log"
    log_level: str = "INFO"


class CommonPortsSettings(BaseModel):
    redis_default: int = 6379
    mysql_default: int = 3306


class CommonSettings(BaseModel):
    time_zone: str = "Asia/Shanghai"
    api_version: str = "v1"
    ports: CommonPortsSettings = CommonPortsSettings()


__all__ = [
    "ModuleSettings",
    "LoggingSettings",
    "CommonPortsSettings",
    "CommonSettings",
]
