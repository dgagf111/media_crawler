from __future__ import annotations

from fastapi import APIRouter, Depends

from media_crawler.api.http_status import HTTPStatus
from media_crawler.api.models.result_vo import ResultVO
from media_crawler.log.logHelper import get_logger
from media_crawler.modules.xhs_downloader.dependencies import get_xhs_downloader_service
from media_crawler.modules.xhs_downloader.schemas import (
    XHSDownloaderDetail,
    XHSDownloaderRequest,
)
from media_crawler.modules.xhs_downloader.services.xhs_downloader_service import (
    XHSDownloaderError,
    XHSDownloaderService,
)

logger = get_logger()

router = APIRouter(prefix="/xhs-downloader", tags=["XHS-Downloader"])


@router.post("/detail")
async def fetch_detail(
    payload: XHSDownloaderRequest,
    service: XHSDownloaderService = Depends(get_xhs_downloader_service),
):
    """提取单个作品详情并可选下载对应文件"""
    if not service.enabled:
        return ResultVO.error(
            code=HTTPStatus.BAD_REQUEST.code,
            message="XHS-Downloader 模块未启用",
        )
    try:
        result: XHSDownloaderDetail = await service.fetch_detail(payload)
        return ResultVO.success(data=result.model_dump())
    except XHSDownloaderError as exc:
        return ResultVO.error(code=HTTPStatus.BAD_REQUEST.code, message=str(exc))
    except Exception as exc:  # pragma: no cover - 保护性兜底
        logger.error("XHS-Downloader 处理作品失败: %s", exc, exc_info=True)
        return ResultVO.error(
            code=HTTPStatus.INTERNAL_SERVER_ERROR.code,
            message="获取作品数据失败",
        )
