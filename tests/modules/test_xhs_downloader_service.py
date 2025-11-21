from __future__ import annotations

import pytest

from media_crawler.config.settings import (
    XHSDownloaderSettings,
    XHSDownloaderStorageSettings,
)
from media_crawler.modules.xhs_downloader.schemas import XHSDownloaderRequest
from media_crawler.modules.xhs_downloader.services.xhs_downloader_service import (
    XHSDownloaderError,
    XHSDownloaderService,
)


class StubXHS:
    def __init__(self, urls: list[str], data: dict | None):
        self.urls = urls
        self.data = data
        self.captured: dict | None = None

    async def extract_links(self, url: str, log):  # pragma: no cover - 简单桩
        return self.urls

    async def _XHS__deal_extract(self, *args, **kwargs):  # pragma: no cover - 简单桩
        self.captured = {
            "args": args,
            "kwargs": kwargs,
        }
        return self.data


def build_settings(enabled: bool = True) -> XHSDownloaderSettings:
    return XHSDownloaderSettings(
        enabled=enabled,
        storage=XHSDownloaderStorageSettings(work_directory="./tmp/xhs", folder_name="Download", name_format="发布时间 作者昵称"),
        default_cookie="a1=demo",
    )


@pytest.mark.asyncio
async def test_fetch_detail_returns_data_when_core_succeeds():
    service = XHSDownloaderService(build_settings())
    stub = StubXHS(urls=["https://www.xiaohongshu.com/explore/demo"], data={"作品ID": "demo"})
    service._client = stub  # type: ignore[attr-defined]
    service._started = True  # type: ignore[attr-defined]
    payload = XHSDownloaderRequest(url="https://www.xiaohongshu.com/explore/demo")

    result = await service.fetch_detail(payload)

    assert result.message == "获取小红书作品数据成功"
    assert result.data == {"作品ID": "demo"}
    assert result.url == "https://www.xiaohongshu.com/explore/demo"


@pytest.mark.asyncio
async def test_fetch_detail_handles_missing_links():
    service = XHSDownloaderService(build_settings())
    service._client = StubXHS(urls=[], data=None)  # type: ignore[attr-defined]
    service._started = True  # type: ignore[attr-defined]

    result = await service.fetch_detail(XHSDownloaderRequest(url="invalid"))

    assert result.message == "提取小红书作品链接失败"
    assert result.data is None


@pytest.mark.asyncio
async def test_fetch_detail_raises_when_disabled():
    service = XHSDownloaderService(build_settings(enabled=False))
    service._client = StubXHS(urls=[], data=None)  # type: ignore[attr-defined]
    service._started = True  # type: ignore[attr-defined]

    with pytest.raises(XHSDownloaderError):
        await service.fetch_detail(XHSDownloaderRequest(url="https://xhslink.com/abc"))
