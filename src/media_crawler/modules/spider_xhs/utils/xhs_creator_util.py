from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict, Tuple

import execjs

from media_crawler.log.logHelper import get_logger

STATIC_PACKAGE = "media_crawler.modules.spider_xhs.assets.static"

logger = get_logger()


def _load_creator_js() -> str:
    try:
        return resources.files(STATIC_PACKAGE).joinpath("xhs_creator_xs.js").read_text("utf-8")
    except FileNotFoundError as exc:  # pragma: no cover
        logger.error("Spider_XHS creator 脚本缺失", exc_info=exc)
        raise


_runtime = execjs.compile(_load_creator_js())


def generate_xs(a1: str, api: str, data: Any = "") -> Tuple[str, int, str | Dict[str, Any]]:
    ret: Dict[str, Any] = _runtime.call("get_request_headers_params", api, data, a1)
    xs, xt = ret["xs"], ret["xt"]
    payload = data
    if data:
        payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return xs, xt, payload


def get_common_headers() -> Dict[str, str]:
    return {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        ),
        "accept": "application/json, text/plain, */*",
        "Host": "edith.xiaohongshu.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua-platform": '"Windows"',
        "authorization": "",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "x-t": "",
        "x-s": "",
        "origin": "https://creator.xiaohongshu.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://creator.xiaohongshu.com/",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "priority": "u=1, i",
    }


def splice_str(api: str, params: Dict[str, Any]) -> str:
    normalized = []
    for key, value in params.items():
        normalized.append(f"{key}={value or ''}")
    return f"{api}?{'&'.join(normalized)}"
