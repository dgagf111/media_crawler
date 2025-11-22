from __future__ import annotations

import logging
from typing import Any, Dict, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .base import CONFIG_LOAD_TRACE, LoadRecord, clear_load_trace, redact_keys
from .models import (
    ApiSettings,
    CacheSettings,
    CommonSettings,
    DatabaseSettings,
    EncryptionSettings,
    LoggingSettings,
    ModuleSettings,
    MonitoringSettings,
    SchedulerSettings,
    SecuritySettings,
    SpiderXHSSettings,
    XHSDownloaderSettings,
)
from .sources import YamlConfigSettingsSource

logger = logging.getLogger(__name__)

SENSITIVE_KEYS = {"password", "secret", "secret_key", "token", "refresh_token"}


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PPT_",
        env_file=".env",
        extra="allow",
        populate_by_name=True,
        env_nested_delimiter="__",
    )

    env: str = "dev"
    config_version: str = Field(default="2024.10", alias="config_version")
    module: ModuleSettings = Field(default_factory=ModuleSettings, alias="module_config")
    logging: LoggingSettings = LoggingSettings()
    scheduler: SchedulerSettings = SchedulerSettings()
    common: CommonSettings = CommonSettings()
    api: ApiSettings = ApiSettings()
    database: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    security: SecuritySettings = SecuritySettings()
    encryption: EncryptionSettings = Field(
        default_factory=EncryptionSettings, alias="encryption_config"
    )
    spider_xhs: SpiderXHSSettings = SpiderXHSSettings()
    xhs_downloader: XHSDownloaderSettings = XHSDownloaderSettings()
    tasks: Dict[str, Any] = Field(default_factory=dict)
    load_trace: List[LoadRecord] = Field(default_factory=list, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        object.__setattr__(self, "load_trace", list(CONFIG_LOAD_TRACE))

    def dump(self, redact_sensitive: bool = True) -> Dict[str, Any]:
        data = self.model_dump(by_alias=True)
        if not redact_sensitive:
            return data
        return redact_keys(data, SENSITIVE_KEYS)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        clear_load_trace()
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


settings = AppSettings()
