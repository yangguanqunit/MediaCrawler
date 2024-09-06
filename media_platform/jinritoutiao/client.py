'''
File Name: client
Create File Time: 2024/5/27 15:20
File Create By Author: Yang Guanqun
Email: yangguanqunit@outlook.com
'''
import asyncio
import copy
import json
import random
import re

import httpx
from typing import Dict, Any, Optional, Callable, List
from urllib.parse import urlencode
from playwright.async_api import Page, BrowserContext

from tools import utils

from .exception import DataFetchError
from tenacity import retry, stop_after_attempt, wait_fixed
class JrttClient:
    def __init__(
            self,
            timeout=10,
            proxies=None,
            *,
            headers: Dict[str, str],
            playwright_page: Page,
            cookie_dict: Dict[str, str],
    ):
        self.proxies = proxies
        self.timeout = timeout
        self.headers = headers
        self._host = "https://www.toutiao.com"
        self.playwright_page = playwright_page
        self.cookie_dict = cookie_dict

        # self.comment_headers = copy.deepcopy(headers)
        self.comment_uri = "/article/v4/tab_comments/"
        self.reply_uri = "/2/comment/v4/reply_list/"

    # Q: method 是个函数吗? A: get and post
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def request(self, method, url, **kwargs) -> Any:
        async with httpx.AsyncClient(proxies=self.proxies) as client:
            response = await client.request(
                method, url, timeout=self.timeout,
                **kwargs
            )
        res: Dict = response.json()
        if res.get("err_no") != 0:
            utils.logger.error(f"[JinritoutiaoClient.request] request {method}:{url} err, res:{res}")
            raise DataFetchError(res.get("msg", "unkonw error"))
        else:
            return res

    # uri: uniform resource identifier  url: uniform resource locator  url 是一种具体的uri
    async def get(self, uri: str, params=None, headers=None) -> Dict:
        final_uri = uri
        if isinstance(params, dict):
            final_uri = (f"{uri}?"
                         f"{urlencode(params)}")

        if headers is None:
            headers = self.headers
        return await self.request(method="GET", url=f"{self._host}{final_uri}", headers=headers)

    async def post(self, uri: str, data: dict) -> Dict:
        # separators 默认是(',', ': ')
        json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        return await self.request(method="POST", url=f"{self._host}{uri}",
                                  data=json_str, headers=self.headers)

    async def pong(self) -> bool:
        utils.logger.info("[JinritoutiaoClient.pong] Begin pong jinritoutiao...")
        ping_flag = False
        try:
            uri = "/api/config"
            resp_data: Dict = await self.request(method="GET", url=f"{self._host}{uri}", headers=self.headers)
            if resp_data.get("login"):
                ping_flag = True
            else:
                utils.logger.error("[JinritoutiaoClient.pong] cookie may be invalid and again login...")
        except Exception as e:
            utils.logger.error(f"[JinritoutiaoClient.pong] Pong jinritoutiao failed: {e}, and try to login again...")
            ping_flag = False
        return ping_flag

    async def update_cookies(self, browser_context: BrowserContext):
        cookie_str, cookie_dict = utils.convert_cookies(await browser_context.cookies())
        self.headers["Cookie"] = cookie_str
        self.cookie_dict = cookie_dict

    async def get_note_all_comments(self, note_id: str, max_interval=3,
                                    callback_comment: Optional[Callable] = None,
                                    callback_reply: Optional[Callable] = None):
        # get count of comments
        comment_info = await self.get_note_comments(note_id, 0, 1, True)
        assert 'total_number' in comment_info.keys(), "not contains total_number"
        total_comments = comment_info['total_number']  # 文章总的评论数
        total_replies = 0
        comment_reply_count = 0
        count = 20
        note_all_comments = []
        for _offset in range(0, total_comments, count):
            batch_note_comments = await self.get_note_comments(note_id, _offset, count, max_interval=max_interval)
            for note_comment in batch_note_comments:
                note_comment = note_comment['comment']
                comment_id = str(note_comment['id'])  # 评论id
                comment_text = note_comment['text']  # 评论的文本，如果只发图片的话，这一项就是空的
                comment_user_id = str(note_comment['user_id'])  # 发布评论的用户的id
                comment_user_name = note_comment['user_name']  # 发布评论的用户的昵称
                comment_user_location = note_comment['publish_loc_info']  # 发布评论的用户的定位
                comment_reply_count = note_comment['reply_count']  # 回复评论的总数量
                comment_create_time = note_comment['create_time']  # 回复创建的时间

                if len(comment_text) == 0:continue
                comment_dict = {
                    'note_id': note_id,
                    'comment_id': comment_id,
                    'user_id': comment_user_id,
                    'user_name': comment_user_name,
                    'ip_location': comment_user_location,
                    'reply_count': comment_reply_count,
                    'text': comment_text,
                    'create_time': comment_create_time,
                }
                note_all_comments.append(comment_dict)

                total_replies = comment_reply_count
                reply_count = 5
                reply_results = []

                for comment_reply_offset in range(0, total_replies, reply_count):
                    batch_replies = await self.get_comment_all_replies(comment_id, comment_reply_offset, reply_count, max_interval)
                    for reply in batch_replies:
                        reply_id = str(reply['id_str'])  # 回复的id
                        reply_text = reply['text']  # 回复的文本内容
                        # reply_content = reply['content']  # 回复的内容（可能含有图片？）
                        reply_user_location = reply['publish_loc_info']  # 回复的用户的定位
                        reply_user_id = str(reply['user']['user_id'])  # 回复的用户的id
                        reply_user_name = reply['user']['name']  # 回复的用户的昵称
                        if reply.get('reply_to_comment', "") == "":
                            # is reply to comment
                            reply_to = ""
                            reply_type = False
                        else:
                            # is reply to reply
                            reply_to = reply['reply_to_comment']['id_str']
                            reply_type = True
                        reply_create_time = reply['create_time']

                        if len(reply_text) == 0: continue
                        reply_dict = {
                            'note_id': note_id,
                            'comment_id': comment_id,
                            'reply_id': reply_id,
                            'user_id': reply_user_id,
                            'user_name': reply_user_name,
                            'ip_location': reply_user_location,
                            'text': reply_text,
                            'to_reply': reply_type,
                            'to_reply_id': reply_to,
                            'create_time': reply_create_time,
                        }
                        reply_results.append(reply_dict)
                # 回复入库存储
                if callback_reply:
                    await callback_reply(note_id, reply_results)


        # 评论入库存储
        if callback_comment:
            await callback_comment(note_id, note_all_comments)


    async def get_note_comments(self, note_id: str, offset=0, count=20, init=False, max_interval=3):
        params = {
            "aid": "24",
            "app_name": "toutiao_web",
            "offset": f"{offset}",
            "count": f"{count}",
            "group_id": note_id,
            "item_id": note_id
        }
        uri = self.comment_uri
        headers = self.headers
        await asyncio.sleep(random.randrange(2, max_interval))
        try:
            comments = await self.get(uri, params, headers)
        except httpx.TimeoutException:
            utils.logger.error(f"connection timeout when visit {uri} in comment")
            return []
        except httpx.RequestError:
            utils.logger.error(f"connection timeout when visit {uri} in comment")
            return []
        comments_data = comments['data']
        if init:
            return comments
        return comments_data

    async def get_comment_all_replies(self, comment_id: str, offset=0, count=5, max_interval=3):
        params = {
            "aid": "24",
            "app_name": "toutiao_web",
            "id": f"{comment_id}",
            "offset": f"{offset}",
            "count": f"{count}",
            "repost": "0"
        }
        uri = self.reply_uri
        headers = self.headers
        await asyncio.sleep(random.randrange(1, max_interval))
        try:
            replies = await self.get(uri, params, headers)
        except httpx.TimeoutException:
            utils.logger.error(f"connection timeout when visit {uri} in reply")
            return []
        except httpx.RequestError:
            utils.logger.error(f"connection timeout when visit {uri} in reply")
            return []
        replies_data = replies['data']['data']
        if not replies_data:
            return []
        return replies_data

    async def get_note_info_by_id(self, note_id: str) -> Dict:
        url = f"{self._host}/w/{note_id}"
        async with httpx.AsyncClient(proxies=self.proxies) as client:
            response = await client.request(
                "GET", url, timeout=self.timeout, headers=self.headers
            )
            if response.status_code != 200:
                raise DataFetchError(f"get jinritoutiao detail err: {response.text}")
            match = re.search(r'var \$render_data = (\[.*?\])\[0\]', response.text, re.DOTALL)
            if match:
                render_data_json = match.group(1)
                render_data_dict = json.loads(render_data_json)
                note_detail = render_data_dict[0].get("status")
                note_item = {
                    "blog": note_detail
                }
                return note_item
            else:
                utils.logger.info(f"[JinritoutiaoClient.get_note_info_by_id] 未找到$render_data的值")
                return dict()


