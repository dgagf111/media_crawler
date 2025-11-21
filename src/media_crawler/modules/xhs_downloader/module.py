from __future__ import annotations

from fastapi import FastAPI

from media_crawler.log.logHelper import get_logger
from media_crawler.modules.base import BaseModule
from media_crawler.modules.xhs_downloader.dependencies import get_xhs_downloader_service

logger = get_logger()


class XHSDownloaderModule:
    async def on_startup(self, app: FastAPI) -> None:
        service = get_xhs_downloader_service()
        await service.startup()
        if not service.enabled:
            return
        app.state.xhs_downloader_service = service
        logger.info("XHS-Downloader 模块初始化完成")

    async def on_shutdown(self, app: FastAPI) -> None:
        service = get_xhs_downloader_service()
        await service.shutdown()
        logger.info("XHS-Downloader 模块已卸载")


def get_module() -> BaseModule:
    return XHSDownloaderModule()
