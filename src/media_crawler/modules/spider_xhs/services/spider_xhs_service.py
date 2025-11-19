from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence

from media_crawler.config.settings import SpiderXHSSettings
from media_crawler.log.logHelper import get_logger
from media_crawler.modules.spider_xhs.clients.pc_client import SpiderXHSPCClient
from media_crawler.modules.spider_xhs.schemas import (
    SpiderNote,
    SpiderNoteCollection,
    SpiderNoteResult,
)
from media_crawler.modules.spider_xhs.utils.data_util import (
    download_note,
    handle_note_info,
    save_to_xlsx,
)

SaveChoice = Literal["none", "media", "media-image", "media-video", "excel", "all"]


class SpiderXHSError(Exception):
    """Spider_XHS 运行异常"""


@dataclass
class SpiderXHSStorage:
    media_dir: Path
    excel_dir: Path

    @classmethod
    def from_settings(cls, base_dir: str, media_subdir: str, excel_subdir: str) -> "SpiderXHSStorage":
        root = Path(base_dir).expanduser().resolve()
        media_path = (root / media_subdir).resolve()
        excel_path = (root / excel_subdir).resolve()
        media_path.mkdir(parents=True, exist_ok=True)
        excel_path.mkdir(parents=True, exist_ok=True)
        return cls(media_dir=media_path, excel_dir=excel_path)


class SpiderXHSService:
    def __init__(
        self,
        settings: SpiderXHSSettings,
        client: SpiderXHSPCClient | None = None,
    ):
        self._settings = settings
        self._client = client or SpiderXHSPCClient()
        storage_settings = settings.storage
        self._storage = SpiderXHSStorage.from_settings(
            storage_settings.base_directory,
            storage_settings.media_subdir,
            storage_settings.excel_subdir,
        )
        self._logger = get_logger()

    def _resolve_cookies(self, cookies_override: str | None) -> str:
        if cookies_override:
            return cookies_override
        if self._settings.default_cookies:
            return self._settings.default_cookies
        raise SpiderXHSError("Spider_XHS 运行需要提供 cookies 或在配置中设置默认值")

    def _build_excel_name(self, excel_name: str | None, fallback: str) -> str:
        if excel_name:
            return excel_name
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"{fallback}_{timestamp}"

    def _should_save_media(self, save_choice: SaveChoice) -> bool:
        return save_choice in {"media", "media-image", "media-video", "all"}

    def _should_save_excel(self, save_choice: SaveChoice) -> bool:
        return save_choice in {"excel", "all"}

    def fetch_note(
        self,
        note_url: str,
        cookies_override: str | None = None,
        proxies: Optional[Dict[str, str]] = None,
    ) -> SpiderNote:
        cookies_str = self._resolve_cookies(cookies_override)
        success, msg, note_info = self._client.get_note_info(note_url, cookies_str, proxies)
        if not success or not note_info:
            raise SpiderXHSError(f"获取笔记失败: {msg}")
        items = note_info.get("data", {}).get("items", [])
        if not items:
            raise SpiderXHSError("笔记数据为空")
        note_payload = items[0]
        note_payload["url"] = note_url
        parsed = handle_note_info(note_payload)
        return SpiderNote(**parsed)

    def fetch_notes(
        self,
        note_urls: Sequence[str],
        save_choice: SaveChoice = "none",
        excel_name: str | None = None,
        cookies_override: str | None = None,
        proxies: Optional[Dict[str, str]] = None,
    ) -> SpiderNoteCollection:
        results: List[SpiderNoteResult] = []
        cache: List[Dict[str, Any]] = []
        for note_url in note_urls:
            try:
                note = self.fetch_note(note_url, cookies_override, proxies)
            except SpiderXHSError as exc:
                self._logger.error(f"抓取笔记 {note_url} 失败: {exc}")
                continue
            media_path = None
            if self._should_save_media(save_choice):
                media_target = download_note(note.model_dump(), self._storage.media_dir, save_choice)
                media_path = str(media_target)
            cache.append(note.model_dump())
            results.append(SpiderNoteResult(note=note, media_path=media_path))

        excel_path = None
        if cache and self._should_save_excel(save_choice):
            target_name = self._build_excel_name(excel_name, "notes")
            destination = self._storage.excel_dir / f"{target_name}.xlsx"
            save_to_xlsx(cache, destination)
            excel_path = str(destination)
        return SpiderNoteCollection(notes=results, excel_path=excel_path)

    def fetch_user_notes(
        self,
        user_url: str,
        save_choice: SaveChoice = "none",
        cookies_override: str | None = None,
        proxies: Optional[Dict[str, str]] = None,
    ) -> SpiderNoteCollection:
        cookies_str = self._resolve_cookies(cookies_override)
        success, msg, note_refs = self._client.get_user_all_notes(user_url, cookies_str, proxies)
        if not success:
            raise SpiderXHSError(f"获取用户笔记失败: {msg}")
        note_urls = []
        for item in note_refs:
            note_id = item.get("note_id")
            token = item.get("xsec_token")
            if not note_id or not token:
                continue
            note_urls.append(f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={token}")
        excel_name = None
        if note_urls and self._should_save_excel(save_choice):
            excel_name = user_url.rstrip("/").split("/")[-1].split("?")[0]
        return self.fetch_notes(note_urls, save_choice, excel_name, cookies_override, proxies)

    def search_notes(
        self,
        query: str,
        require_num: int,
        save_choice: SaveChoice = "none",
        excel_name: str | None = None,
        cookies_override: str | None = None,
        proxies: Optional[Dict[str, str]] = None,
        sort_type_choice: int = 0,
        note_type: int = 0,
        note_time: int = 0,
        note_range: int = 0,
        pos_distance: int = 0,
        geo: Optional[Dict[str, object]] = None,
    ) -> SpiderNoteCollection:
        cookies_str = self._resolve_cookies(cookies_override)
        success, msg, items = self._client.search_some_note(
            query,
            require_num,
            cookies_str,
            sort_type_choice,
            note_type,
            note_time,
            note_range,
            pos_distance,
            geo or "",
            proxies,
        )
        if not success:
            raise SpiderXHSError(f"搜索笔记失败: {msg}")
        note_urls = []
        for item in items:
            if item.get("model_type") != "note":
                continue
            note_id = item.get("id")
            token = item.get("xsec_token")
            if not note_id or not token:
                continue
            note_urls.append(f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={token}")
        excel_label = excel_name or query if self._should_save_excel(save_choice) else None
        return self.fetch_notes(note_urls, save_choice, excel_label, cookies_override, proxies)
