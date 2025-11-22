from __future__ import annotations

import warnings
from typing import Any, Dict, List

from .settings import AppSettings, settings as runtime_settings


class Config:
    """
    Backwards compatible facade around the new AppSettings object.
    Prefer直接使用 `pythonprojecttemplate.config.settings`。
    """

    _instance: Config | None = None

    def __new__(cls, app_settings: AppSettings | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, app_settings: AppSettings | None = None):
        if app_settings is not None:
            self._set_settings(app_settings)
            return

        if getattr(self, "_initialized", False):
            return

        self._set_settings(runtime_settings)

    def _set_settings(self, app_settings: AppSettings) -> None:
        self._settings = app_settings
        self._initialized = True

    def reload(self, app_settings: AppSettings | None = None) -> None:
        """
        Reload configuration, optionally using a caller-provided AppSettings object.
        """
        warnings.warn(
            "Config.reload 已弃用，请直接实例化 AppSettings 或使用 settings，未来版本将移除。",
            DeprecationWarning,
            stacklevel=2,
        )
        self._set_settings(app_settings or AppSettings())

    def _load_config(self, app_settings: AppSettings | None = None) -> None:
        """
        Backwards-compatible alias used by older tests/docs.
        """
        self.reload(app_settings)

    def get_env_config(self) -> Dict[str, Any]:
        return self._settings.model_dump(by_alias=True)

    def get_config(self) -> Dict[str, Any]:
        return self._settings.model_dump(by_alias=True)

    def get_mysql_config(self) -> Dict[str, Any]:
        return self._settings.database.model_dump()

    def get_log_config(self) -> Dict[str, Any]:
        return self._settings.logging.model_dump()

    def get_module_config(self) -> Dict[str, Any]:
        return self._settings.module.model_dump()

    def get_load_modules(self) -> Dict[str, Any]:
        return self.get_module_config()

    def get_scheduler_config(self) -> Dict[str, Any]:
        return self._settings.scheduler.model_dump()

    def get_tasks_config(self) -> Dict[str, Any]:
        return self._settings.tasks

    def get_cache_config(self) -> Dict[str, Any]:
        return self._settings.cache.model_dump()

    def get_monitoring_config(self) -> Dict[str, Any]:
        return self._settings.monitoring.model_dump()

    def get_api_config(self) -> Dict[str, Any]:
        return self._settings.api.model_dump()

    def get_security_config(self) -> Dict[str, Any]:
        return self._settings.security.model_dump()

    def get_time_zone(self) -> str:
        return self._settings.common.time_zone

    def get_common_config(self) -> Dict[str, Any]:
        return self._settings.common.model_dump()

    def get_api_version(self) -> str:
        return self._settings.common.api_version

    def get_load_trace(self) -> List[Any]:
        return getattr(self._settings, "load_trace", [])


config = Config()
