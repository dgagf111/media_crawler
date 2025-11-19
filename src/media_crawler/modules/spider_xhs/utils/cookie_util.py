from __future__ import annotations

from typing import Dict


def trans_cookies(cookies_str: str) -> Dict[str, str]:
    delimiter = "; " if "; " in cookies_str else ";"
    cookies: Dict[str, str] = {}
    for item in cookies_str.split(delimiter):
        if not item.strip():
            continue
        key, *value_parts = item.split("=")
        cookies[key] = "=".join(value_parts)
    return cookies
