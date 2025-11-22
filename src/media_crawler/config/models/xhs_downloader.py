from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel, Field


class XHSDownloaderStorageSettings(BaseModel):
    work_directory: str = "~/data/xhs_downloader"
    folder_name: str = "Download"
    name_format: str = "发布时间 作者昵称 作品标题"


class XHSDownloaderSettings(BaseModel):
    enabled: bool = False
    storage: XHSDownloaderStorageSettings = XHSDownloaderStorageSettings()
    default_cookie: str = ""
    user_agent: Optional[str] = None
    proxy: Optional[str] = None
    timeout_seconds: int = Field(default=10, ge=1, le=60)
    chunk_size: int = Field(default=2 * 1024 * 1024, ge=1024, le=50 * 1024 * 1024)
    max_retry: int = Field(default=5, ge=1, le=10)
    record_data: bool = False
    image_format: str = "PNG"
    image_download: bool = True
    video_download: bool = True
    live_download: bool = False
    folder_mode: bool = False
    download_record: bool = True
    author_archive: bool = False
    write_mtime: bool = False
    language: str = "zh_CN"
    read_cookie: str | int | None = None
    print_logs: bool = True
    mapping_file: Optional[str] = None
    mapping_data: Dict[str, str] = Field(default_factory=dict)


__all__ = ["XHSDownloaderSettings", "XHSDownloaderStorageSettings"]
