from __future__ import annotations

import json
import math
import random
from importlib import resources
from typing import Any, Dict, Tuple

import execjs

from media_crawler.log.logHelper import get_logger

STATIC_PACKAGE = "media_crawler.modules.spider_xhs.assets.static"

logger = get_logger()


def _load_js_source(filename: str) -> str:
    try:
        return resources.files(STATIC_PACKAGE).joinpath(filename).read_text("utf-8")
    except FileNotFoundError as exc:  # pragma: no cover - 磁盘异常
        logger.error(f"Spider_XHS JS 资源缺失: {filename}", exc_info=exc)
        raise


_xs_runtime = execjs.compile(_load_js_source("xhs_xs_xsc_56.js"))
_xray_runtime = execjs.compile(_load_js_source("xhs_xray.js"))


def generate_x_b3_traceid(length: int = 16) -> str:
    charset = "abcdef0123456789"
    return "".join(charset[math.floor(16 * random.random())] for _ in range(length))


def generate_xs_xs_common(a1: str, api: str, data: Any = "") -> Tuple[str, int, str]:
    ret: Dict[str, Any] = _xs_runtime.call("get_request_headers_params", api, data, a1)
    return ret["xs"], ret["xt"], ret["xs_common"]


def generate_xs(a1: str, api: str, data: Any = "") -> Tuple[str, int]:
    ret: Dict[str, Any] = _xs_runtime.call("get_xs", api, data, a1)
    return ret["X-s"], ret["X-t"]


def generate_xray_traceid() -> str:
    return _xray_runtime.call("traceId")


def get_common_headers() -> Dict[str, str]:
    return {
        "authority": "www.xiaohongshu.com",
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
            "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.xiaohongshu.com/",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
    }


def get_request_headers_template() -> Dict[str, str]:
    return {
        "authority": "edith.xiaohongshu.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "pragma": "no-cache",
        "referer": "https://www.xiaohongshu.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        ),
        "x-b3-traceid": "",
        "x-mns": "unload",
        "x-s": "",
        "x-s-common": "",
        "x-t": "",
        "x-xray-traceid": generate_xray_traceid(),
    }


def generate_headers(a1: str, api: str, data: Any = "") -> tuple[Dict[str, str], str | dict]:
    xs, xt, xs_common = generate_xs_xs_common(a1, api, data)
    headers = get_request_headers_template()
    headers["x-s"] = xs
    headers["x-t"] = str(xt)
    headers["x-s-common"] = xs_common
    headers["x-b3-traceid"] = generate_x_b3_traceid()
    if data:
        data = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return headers, data


def generate_request_params(cookies_str: str, api: str, data: Any = "") -> tuple[Dict[str, str], Dict[str, str], str | dict]:
    from media_crawler.modules.spider_xhs.utils.cookie_util import trans_cookies

    cookies = trans_cookies(cookies_str)
    a1 = cookies.get("a1", "")
    headers, data_payload = generate_headers(a1, api, data)
    return headers, cookies, data_payload


def splice_str(api: str, params: Dict[str, Any]) -> str:
    normalized = []
    for key, value in params.items():
        value_str = "" if value is None else str(value)
        normalized.append(f"{key}={value_str}")
    return f"{api}?{'&'.join(normalized)}"
