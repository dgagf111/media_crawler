from __future__ import annotations

from fastapi import FastAPI

from media_crawler.log.logHelper import get_logger
from media_crawler.modules.base import BaseModule
from media_crawler.modules.spider_xhs.dependencies import get_spider_xhs_service

logger = get_logger()


class SpiderXHSModule:
    async def on_startup(self, app: FastAPI) -> None:
        service = get_spider_xhs_service()
        app.state.spider_xhs_service = service
        logger.info("Spider_XHS 模块初始化完成")

    async def on_shutdown(self, app: FastAPI) -> None:
        logger.info("Spider_XHS 模块已卸载")


def get_module() -> BaseModule:
    return SpiderXHSModule()
