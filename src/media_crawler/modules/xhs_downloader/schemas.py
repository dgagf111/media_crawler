from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class XHSDownloaderRequest(BaseModel):
    url: str = Field(..., description="小红书作品链接，支持包含 xhslink 形式")
    download: bool = Field(default=False, description="是否下载作品文件")
    index: Optional[List[int]] = Field(
        default=None,
        description="需要下载的图文序号，从 1 开始，未设置则下载全部",
    )
    cookie: Optional[str] = Field(default=None, description="覆盖默认 Cookie")
    proxy: Optional[str] = Field(default=None, description="HTTP/SOCKS 代理地址")
    skip_downloaded: bool = Field(
        default=False,
        description="如果已经存在下载记录则跳过处理",
    )

    @field_validator("url", mode="before")
    @classmethod
    def _trim_url(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("index", mode="before")
    @classmethod
    def _coerce_index(cls, value: Any) -> Optional[List[int]]:
        if value is None or value == "":
            return None
        if isinstance(value, str):
            raw_values = value.replace(",", " ").split()
        elif isinstance(value, (list, tuple)):
            raw_values = value
        else:
            return None
        cleaned: List[int] = []
        for item in raw_values:
            try:
                cleaned.append(int(item))
            except (TypeError, ValueError):
                continue
        return cleaned or None


class XHSDownloaderDetail(BaseModel):
    url: str = Field(..., description="实际处理的作品链接")
    message: str
    data: Optional[Dict[str, Any]] = Field(default=None, description="作品详情数据")
