from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SpiderNote(BaseModel):
    note_id: str
    note_url: str
    note_type: str
    user_id: str
    home_url: str
    nickname: str
    avatar: Optional[str] = None
    title: str
    desc: str
    liked_count: int
    collected_count: int
    comment_count: int
    share_count: int
    video_cover: Optional[str] = None
    video_addr: Optional[str] = None
    image_list: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    upload_time: str
    ip_location: str


class SpiderNoteResult(BaseModel):
    note: SpiderNote
    media_path: Optional[str] = None


class SpiderNoteCollection(BaseModel):
    notes: List[SpiderNoteResult] = Field(default_factory=list)
    excel_path: Optional[str] = None
