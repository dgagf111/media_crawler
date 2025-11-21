from __future__ import annotations

from functools import lru_cache

from media_crawler.config.settings import settings
from media_crawler.modules.xhs_downloader.services.xhs_downloader_service import (
    XHSDownloaderService,
)


@lru_cache(maxsize=1)
def get_xhs_downloader_service() -> XHSDownloaderService:
    return XHSDownloaderService(settings.xhs_downloader)
