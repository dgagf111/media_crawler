from __future__ import annotations

from functools import lru_cache

from media_crawler.config.settings import settings
from media_crawler.modules.spider_xhs.services.spider_xhs_service import SpiderXHSService


@lru_cache(maxsize=1)
def get_spider_xhs_service() -> SpiderXHSService:
    return SpiderXHSService(settings.spider_xhs)
