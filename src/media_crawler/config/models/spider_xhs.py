from __future__ import annotations

from pydantic import BaseModel


class SpiderXHSStorageSettings(BaseModel):
    base_directory: str = "~/data/spider_xhs"
    media_subdir: str = "media"
    excel_subdir: str = "excel"


class SpiderXHSSettings(BaseModel):
    enabled: bool = False
    default_cookies: str = ""
    storage: SpiderXHSStorageSettings = SpiderXHSStorageSettings()


__all__ = ["SpiderXHSSettings", "SpiderXHSStorageSettings"]
