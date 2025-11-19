from __future__ import annotations

from pathlib import Path

import pytest

from media_crawler.config.settings import SpiderXHSSettings, SpiderXHSStorageSettings
from media_crawler.modules.spider_xhs.services.spider_xhs_service import (
    SpiderXHSError,
    SpiderXHSService,
)


def build_note_payload() -> dict:
    return {
        "id": "note123",
        "url": "https://www.xiaohongshu.com/explore/note123",
        "note_card": {
            "type": "normal",
            "user": {"user_id": "user1", "nickname": "tester", "avatar": "http://avatar"},
            "title": "测试标题",
            "desc": "测试描述",
            "interact_info": {
                "liked_count": 1,
                "collected_count": 2,
                "comment_count": 3,
                "share_count": 4,
            },
            "image_list": [
                {"info_list": [{}, {"url": "http://image"}]},
            ],
            "tag_list": [{"name": "tag1"}],
            "time": 1_700_000_000_000,
        },
    }


class DummyClient:
    def __init__(self, note_payload: dict):
        self.note_payload = note_payload

    def get_note_info(self, note_url, cookies_str, proxies=None):
        self.note_payload["url"] = note_url
        return True, "ok", {"data": {"items": [self.note_payload]}}

    def get_user_all_notes(self, user_url, cookies_str, proxies=None):
        return True, "ok", [{"note_id": "note123", "xsec_token": "token"}]

    def search_some_note(
        self,
        query,
        require_num,
        cookies_str,
        sort_type_choice,
        note_type,
        note_time,
        note_range,
        pos_distance,
        geo,
        proxies=None,
    ):
        return True, "ok", [{"model_type": "note", "id": "note123", "xsec_token": "token"}]


def build_service(tmp_path: Path) -> SpiderXHSService:
    settings = SpiderXHSSettings(
        default_cookies="a1=mock;",
        storage=SpiderXHSStorageSettings(
            base_directory=str(tmp_path),
            media_subdir="media",
            excel_subdir="excel",
        ),
    )
    client = DummyClient(build_note_payload())
    return SpiderXHSService(settings, client=client)


def test_fetch_note_returns_structured_data(tmp_path: Path):
    service = build_service(tmp_path)
    result = service.fetch_note("https://www.xiaohongshu.com/explore/note123?xsec_token=token")
    assert result.note_id == "note123"
    assert result.note_type == "图集"


def test_fetch_notes_can_export_excel(tmp_path: Path):
    service = build_service(tmp_path)
    collection = service.fetch_notes(
        ["https://www.xiaohongshu.com/explore/note123?xsec_token=token"],
        save_choice="excel",
    )
    assert collection.excel_path is not None
    assert Path(collection.excel_path).exists()


def test_missing_cookies_raise_error(tmp_path: Path):
    settings = SpiderXHSSettings(
        default_cookies="",
        storage=SpiderXHSStorageSettings(
            base_directory=str(tmp_path),
            media_subdir="media",
            excel_subdir="excel",
        ),
    )
    service = SpiderXHSService(settings, client=DummyClient(build_note_payload()))
    with pytest.raises(SpiderXHSError):
        service.fetch_note("https://www.xiaohongshu.com/explore/note123?xsec_token=token")
