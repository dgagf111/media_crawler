from __future__ import annotations

import requests

from media_crawler.modules.spider_xhs.utils.cookie_util import trans_cookies
from media_crawler.modules.spider_xhs.utils.xhs_creator_util import (
    generate_xs,
    get_common_headers,
    splice_str,
)

class SpiderXHSCreatorClient:
    def __init__(self):
        self.base_url = "https://edith.xiaohongshu.com"


    # page: 页数
    # time: 最近几天的时间
    def get_publish_note_info(self, page: int, cookies_str: str):
        success = False
        msg = "成功"
        res_json = None

        try:
            api = "/web_api/sns/v5/creator/note/user/posted"
            params = {
                "tab": "0",
            }
            if page >= 0:
                params["page"] = str(page)
            splice_api = splice_str(api, params)
            headers = get_common_headers()
            cookies = trans_cookies(cookies_str)
            xs, xt, _ = generate_xs(cookies["a1"], splice_api, "")
            headers["x-s"], headers["x-t"] = xs, str(xt)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, timeout=30)
            res_json = response.json()
            success = res_json["success"]
        except Exception as e:
            success, msg = False, str(e)
        return success, msg, res_json


    # 获取全部的发布信息
    def get_all_publish_note_info(self, cookies_str: str):
        page = None
        notes = []
        while True:
            success, msg, res_json = self.get_publish_note_info(page, cookies_str)
            if not success:
                return False, msg, notes
            notes += res_json["data"]["notes"]
            page = res_json["data"]["page"]
            if page == -1:
                break
        return True, "成功", notes
