from __future__ import annotations

from typing import Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, model_validator

from media_crawler.api.http_status import HTTPStatus
from media_crawler.api.models.result_vo import ResultVO
from media_crawler.modules.spider_xhs.dependencies import get_spider_xhs_service
from media_crawler.modules.spider_xhs.schemas import SpiderNoteCollection
from media_crawler.modules.spider_xhs.services.spider_xhs_service import (
    SaveChoice,
    SpiderXHSError,
    SpiderXHSService,
)

router = APIRouter(prefix="/spider-xhs", tags=["Spider_XHS"])


class SpiderXHSBaseRequest(BaseModel):
    save_choice: SaveChoice = Field(default="none", description="保存选项")
    excel_name: Optional[str] = Field(default=None, description="导出 Excel 名称")
    cookies: Optional[str] = Field(default=None, description="额外的 cookies")
    proxies: Optional[Dict[str, str]] = Field(default=None, description="requests 代理配置")


class SpiderNoteBatchRequest(SpiderXHSBaseRequest):
    note_urls: list[str] = Field(..., min_length=1, description="笔记链接列表")


class SpiderUserNotesRequest(SpiderXHSBaseRequest):
    user_url: str = Field(..., description="用户主页链接")


class SpiderSearchRequest(SpiderXHSBaseRequest):
    query: str = Field(..., min_length=1, description="搜索关键字")
    require_num: int = Field(default=10, ge=1, le=1000, description="需要的笔记数量")
    sort_type_choice: int = Field(default=0, ge=0, le=4)
    note_type: int = Field(default=0, ge=0, le=2)
    note_time: int = Field(default=0, ge=0, le=3)
    note_range: int = Field(default=0, ge=0, le=3)
    pos_distance: int = Field(default=0, ge=0, le=2)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @model_validator(mode="after")
    def validate_geo(self) -> "SpiderSearchRequest":
        if self.pos_distance in {1, 2} and (self.latitude is None or self.longitude is None):
            raise ValueError("指定距离筛选时必须提供经纬度")
        return self

    def geo_payload(self) -> Optional[Dict[str, float]]:
        if self.latitude is None or self.longitude is None:
            return None
        return {"latitude": self.latitude, "longitude": self.longitude}


def _build_success_response(result: SpiderNoteCollection):
    return ResultVO.success(data=result.model_dump())


def _build_error_response(exc: SpiderXHSError):
    return ResultVO.error(code=HTTPStatus.BAD_REQUEST.code, message=str(exc))


@router.post("/notes:batch")
async def batch_notes(
    payload: SpiderNoteBatchRequest,
    service: SpiderXHSService = Depends(get_spider_xhs_service),
):
    """
    批量获取指定笔记的详细信息并可选导出。
    """
    try:
        result = service.fetch_notes(
            note_urls=payload.note_urls,
            save_choice=payload.save_choice,
            excel_name=payload.excel_name,
            cookies_override=payload.cookies,
            proxies=payload.proxies,
        )
        return _build_success_response(result)
    except SpiderXHSError as exc:
        return _build_error_response(exc)


@router.post("/user-notes")
async def user_notes(
    payload: SpiderUserNotesRequest,
    service: SpiderXHSService = Depends(get_spider_xhs_service),
):
    """
    获取指定用户的全部笔记。
    """
    try:
        result = service.fetch_user_notes(
            user_url=payload.user_url,
            save_choice=payload.save_choice,
            cookies_override=payload.cookies,
            proxies=payload.proxies,
        )
        return _build_success_response(result)
    except SpiderXHSError as exc:
        return _build_error_response(exc)


@router.post("/search")
async def search_notes(
    payload: SpiderSearchRequest,
    service: SpiderXHSService = Depends(get_spider_xhs_service),
):
    """
    搜索关键字，并批量导出匹配的笔记。
    """
    try:
        result = service.search_notes(
            query=payload.query,
            require_num=payload.require_num,
            save_choice=payload.save_choice,
            excel_name=payload.excel_name,
            cookies_override=payload.cookies,
            proxies=payload.proxies,
            sort_type_choice=payload.sort_type_choice,
            note_type=payload.note_type,
            note_time=payload.note_time,
            note_range=payload.note_range,
            pos_distance=payload.pos_distance,
            geo=payload.geo_payload(),
        )
        return _build_success_response(result)
    except SpiderXHSError as exc:
        return _build_error_response(exc)
