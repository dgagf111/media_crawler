from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from media_crawler.config.settings import XHSDownloaderSettings
from media_crawler.log.logHelper import get_logger

from media_crawler.modules.xhs_downloader.core.application import XHS
from media_crawler.modules.xhs_downloader.schemas import (
    XHSDownloaderDetail,
    XHSDownloaderRequest,
)

logger = get_logger()


class XHSDownloaderError(Exception):
    """XHS-Downloader 模块运行异常"""


class XHSDownloaderService:
    def __init__(self, settings: XHSDownloaderSettings):
        self._settings = settings
        self._client: Optional[XHS] = None
        self._started = False

    @property
    def enabled(self) -> bool:
        return self._settings.enabled

    @property
    def started(self) -> bool:
        return self._started

    async def startup(self) -> None:
        if not self.enabled:
            logger.info("XHS-Downloader 模块未启用，跳过初始化")
            return
        if self._started:
            return
        runtime_config = self._build_runtime_kwargs()
        self._client = XHS(**runtime_config)
        await self._client.__aenter__()
        self._started = True
        logger.info("XHS-Downloader 服务初始化完成")

    async def shutdown(self) -> None:
        if not self._client:
            return
        try:
            await self._client.__aexit__(None, None, None)
        finally:
            self._client = None
            self._started = False
            logger.info("XHS-Downloader 服务已关闭")

    def _build_runtime_kwargs(self) -> Dict[str, Any]:
        storage_root = Path(self._settings.storage.work_directory).expanduser()
        mapping_data = self._load_mapping_data()
        return {
            "mapping_data": mapping_data,
            "work_path": str(storage_root),
            "folder_name": self._settings.storage.folder_name,
            "name_format": self._settings.storage.name_format,
            "user_agent": self._settings.user_agent,
            "cookie": self._settings.default_cookie,
            "proxy": self._settings.proxy,
            "timeout": self._settings.timeout_seconds,
            "chunk": self._settings.chunk_size,
            "max_retry": self._settings.max_retry,
            "record_data": self._settings.record_data,
            "image_format": self._settings.image_format,
            "image_download": self._settings.image_download,
            "video_download": self._settings.video_download,
            "live_download": self._settings.live_download,
            "folder_mode": self._settings.folder_mode,
            "download_record": self._settings.download_record,
            "author_archive": self._settings.author_archive,
            "write_mtime": self._settings.write_mtime,
            "language": self._settings.language,
            "read_cookie": self._settings.read_cookie,
            "_print": self._settings.print_logs,
        }

    def _load_mapping_data(self) -> Dict[str, str]:
        mapping: Dict[str, str] = dict(self._settings.mapping_data)
        file_path = self._settings.mapping_file
        if not file_path:
            return mapping
        path = Path(file_path).expanduser()
        if not path.is_file():
            logger.warning("XHS-Downloader 映射文件 %s 不存在，忽略", path)
            return mapping
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - 仅记录日志
            logger.warning("读取 XHS-Downloader 映射文件失败: %s", exc)
            return mapping
        if isinstance(raw, dict):
            mapping.update({str(k): str(v) for k, v in raw.items()})
        else:  # pragma: no cover - 仅日志
            logger.warning("XHS-Downloader 映射文件 %s 内容需为字典，实际为 %s", path, type(raw))
        return mapping

    def _require_client(self) -> XHS:
        if not self._client:
            raise XHSDownloaderError("XHS-Downloader 服务尚未初始化")
        return self._client

    async def fetch_detail(self, payload: XHSDownloaderRequest) -> XHSDownloaderDetail:
        if not self.enabled:
            raise XHSDownloaderError("XHS-Downloader 模块未启用")
        client = self._require_client()
        try:
            urls = await client.extract_links(payload.url, None)
        except Exception as exc:  # pragma: no cover - 保护性兜底
            logger.error("解析作品链接失败: %s", exc, exc_info=True)
            raise XHSDownloaderError("提取小红书作品链接失败") from exc
        if not urls:
            return XHSDownloaderDetail(
                url=payload.url,
                message="提取小红书作品链接失败",
                data=None,
            )
        target = urls[0]
        data = await self._invoke_core(target, payload)
        message = "获取小红书作品数据成功" if data else "获取小红书作品数据失败"
        return XHSDownloaderDetail(url=target, message=message, data=data)

    async def _invoke_core(
        self,
        url: str,
        payload: XHSDownloaderRequest,
    ) -> Optional[Dict[str, Any]]:
        client = self._require_client()
        # 直接调用底层私有方法以复用 cookie/proxy 覆盖逻辑
        return await client._XHS__deal_extract(  # type: ignore[attr-defined]
            url,
            payload.download,
            payload.index,
            None,
            None,
            not payload.skip_downloaded,
            payload.cookie,
            payload.proxy,
        )
