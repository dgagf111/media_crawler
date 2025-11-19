from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List

import openpyxl
import requests
from retry import retry

from media_crawler.log.logHelper import get_logger

logger = get_logger()

ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")


def norm_str(value: str) -> str:
    cleaned = re.sub(r"|[\\/:*?\"<>| ]+", "", value)
    return cleaned.replace("\n", "").replace("\r", "")


def norm_text(value: str) -> str:
    return ILLEGAL_CHARACTERS_RE.sub("", value)


def timestamp_to_str(timestamp: int) -> str:
    time_local = time.localtime(timestamp / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def handle_user_info(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    basic_info = data.get("basic_info", {})
    interactions = data.get("interactions", [])

    gender_code = basic_info.get("gender")
    gender = "未知"
    if gender_code == 0:
        gender = "男"
    elif gender_code == 1:
        gender = "女"

    tags = [tag.get("name") for tag in data.get("tags", []) if isinstance(tag, dict)]

    return {
        "user_id": user_id,
        "home_url": f"https://www.xiaohongshu.com/user/profile/{user_id}",
        "nickname": basic_info.get("nickname", ""),
        "avatar": basic_info.get("imageb"),
        "red_id": basic_info.get("red_id"),
        "gender": gender,
        "ip_location": basic_info.get("ip_location", "未知"),
        "desc": basic_info.get("desc", ""),
        "follows": interactions[0]["count"] if len(interactions) > 0 else 0,
        "fans": interactions[1]["count"] if len(interactions) > 1 else 0,
        "interaction": interactions[2]["count"] if len(interactions) > 2 else 0,
        "tags": tags,
    }


def handle_note_info(data: Dict[str, Any]) -> Dict[str, Any]:
    note_card = data.get("note_card", {})
    note_type = "图集" if note_card.get("type") == "normal" else "视频"
    user = note_card.get("user", {})
    image_list = []
    for image in note_card.get("image_list", []):
        try:
            image_list.append(image["info_list"][1]["url"])
        except Exception:
            continue

    video_cover = image_list[0] if image_list else None
    video_addr = None
    if note_type == "视频":
        video = note_card.get("video", {}).get("consumer", {})
        origin_key = video.get("origin_video_key")
        if origin_key:
            video_addr = f"https://sns-video-bd.xhscdn.com/{origin_key}"

    tags = [tag.get("name") for tag in note_card.get("tag_list", []) if isinstance(tag, dict)]
    title = note_card.get("title", "").strip() or "无标题"

    return {
        "note_id": data.get("id"),
        "note_url": data.get("url"),
        "note_type": note_type,
        "user_id": user.get("user_id"),
        "home_url": f"https://www.xiaohongshu.com/user/profile/{user.get('user_id')}",
        "nickname": user.get("nickname"),
        "avatar": user.get("avatar"),
        "title": title,
        "desc": note_card.get("desc", ""),
        "liked_count": note_card.get("interact_info", {}).get("liked_count", 0),
        "collected_count": note_card.get("interact_info", {}).get("collected_count", 0),
        "comment_count": note_card.get("interact_info", {}).get("comment_count", 0),
        "share_count": note_card.get("interact_info", {}).get("share_count", 0),
        "video_cover": video_cover,
        "video_addr": video_addr,
        "image_list": image_list,
        "tags": tags,
        "upload_time": timestamp_to_str(note_card.get("time", 0)),
        "ip_location": note_card.get("ip_location", "未知"),
    }


def handle_comment_info(data: Dict[str, Any]) -> Dict[str, Any]:
    user_info = data.get("user_info", {})
    pictures: List[str] = []
    for picture in data.get("pictures", []):
        try:
            pictures.append(picture["info_list"][1]["url"])
        except Exception:
            continue
    return {
        "note_id": data.get("note_id"),
        "note_url": data.get("note_url"),
        "comment_id": data.get("id"),
        "user_id": user_info.get("user_id"),
        "home_url": f"https://www.xiaohongshu.com/user/profile/{user_info.get('user_id')}",
        "nickname": user_info.get("nickname"),
        "avatar": user_info.get("image"),
        "content": data.get("content", ""),
        "show_tags": data.get("show_tags", []),
        "like_count": data.get("like_count", 0),
        "upload_time": timestamp_to_str(data.get("create_time", 0)),
        "ip_location": data.get("ip_location", "未知"),
        "pictures": pictures,
    }


def save_to_xlsx(datas: Iterable[Dict[str, Any]], file_path: Path, data_type: str = "note") -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    if data_type == "note":
        headers = [
            "笔记id",
            "笔记url",
            "笔记类型",
            "用户id",
            "用户主页url",
            "昵称",
            "头像url",
            "标题",
            "描述",
            "点赞数量",
            "收藏数量",
            "评论数量",
            "分享数量",
            "视频封面url",
            "视频地址url",
            "图片地址url列表",
            "标签",
            "上传时间",
            "ip归属地",
        ]
    elif data_type == "user":
        headers = [
            "用户id",
            "用户主页url",
            "用户名",
            "头像url",
            "小红书号",
            "性别",
            "ip地址",
            "介绍",
            "关注数量",
            "粉丝数量",
            "作品被赞和收藏数量",
            "标签",
        ]
    else:
        headers = [
            "笔记id",
            "笔记url",
            "评论id",
            "用户id",
            "用户主页url",
            "昵称",
            "头像url",
            "评论内容",
            "评论标签",
            "点赞数量",
            "上传时间",
            "ip归属地",
            "图片地址url列表",
        ]
    ws.append(headers)
    for record in datas:
        normalized = {k: norm_text(str(v)) for k, v in record.items()}
        ws.append(list(normalized.values()))
    file_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(file_path)
    logger.info(f"Spider_XHS 数据保存至 {file_path}")


def download_media(path: Path, name: str, url: str, media_type: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if media_type == "image":
        content = requests.get(url, timeout=60).content
        (path / f"{name}.jpg").write_bytes(content)
        return
    if media_type == "video":
        response = requests.get(url, stream=True, timeout=60)
        chunk_size = 1024 * 1024
        with (path / f"{name}.mp4").open("wb") as handle:
            for chunk in response.iter_content(chunk_size=chunk_size):
                handle.write(chunk)


def save_user_detail(user: Dict[str, Any], path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    with (path / "detail.txt").open("w", encoding="utf-8") as handle:
        lines = [
            f"用户id: {user['user_id']}",
            f"用户主页url: {user['home_url']}",
            f"用户名: {user['nickname']}",
            f"头像url: {user['avatar']}",
            f"小红书号: {user['red_id']}",
            f"性别: {user['gender']}",
            f"ip地址: {user['ip_location']}",
            f"介绍: {user['desc']}",
            f"关注数量: {user['follows']}",
            f"粉丝数量: {user['fans']}",
            f"作品被赞和收藏数量: {user['interaction']}",
            f"标签: {user['tags']}",
        ]
        handle.write("\n".join(lines))


def save_note_detail(note: Dict[str, Any], path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    with (path / "detail.txt").open("w", encoding="utf-8") as handle:
        lines = [
            f"笔记id: {note['note_id']}",
            f"笔记url: {note['note_url']}",
            f"笔记类型: {note['note_type']}",
            f"用户id: {note['user_id']}",
            f"用户主页url: {note['home_url']}",
            f"昵称: {note['nickname']}",
            f"头像url: {note['avatar']}",
            f"标题: {note['title']}",
            f"描述: {note['desc']}",
            f"点赞数量: {note['liked_count']}",
            f"收藏数量: {note['collected_count']}",
            f"评论数量: {note['comment_count']}",
            f"分享数量: {note['share_count']}",
            f"视频封面url: {note['video_cover']}",
            f"视频地址url: {note['video_addr']}",
            f"图片地址url列表: {note['image_list']}",
            f"标签: {note['tags']}",
            f"上传时间: {note['upload_time']}",
            f"ip归属地: {note['ip_location']}",
        ]
        handle.write("\n".join(lines))


@retry(tries=3, delay=1)
def download_note(note_info: Dict[str, Any], base_path: Path, save_choice: str) -> Path:
    note_id = note_info["note_id"]
    user_id = note_info["user_id"]
    title = norm_str(note_info["title"])[:40] or "无标题"
    nickname = norm_str(note_info["nickname"])[:20]
    save_path = base_path / f"{nickname}_{user_id}" / f"{title}_{note_id}"
    save_path.mkdir(parents=True, exist_ok=True)
    (save_path / "info.json").write_text(json.dumps(note_info, ensure_ascii=False), encoding="utf-8")
    save_note_detail(note_info, save_path)

    note_type = note_info["note_type"]
    if note_type == "图集" and save_choice in ["media", "media-image", "all"]:
        for index, img_url in enumerate(note_info["image_list"]):
            download_media(save_path, f"image_{index}", img_url, "image")
    elif note_type == "视频" and save_choice in ["media", "media-video", "all"]:
        download_media(save_path, "cover", note_info["video_cover"], "image")
        download_media(save_path, "video", note_info["video_addr"], "video")
    return save_path
