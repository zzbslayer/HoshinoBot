import httpx
import json
import time
import asyncio
from hoshino import logger

'''
TODO: 不同类型解析
B博博文类型
1: 转发
    转发文本
    转发文本+图片
    转发长文本
2: 原创，文本+图片
4: 原创，纯文本
8: 分享bilibili视频
64: 专栏
'''

parse_type = [1, 2, 4, 8]

class BilibiliSpider(object):
    def __init__(self, config):
        self.user_id = config["user_id"]
        self.received_dynamic_ids = []
        self.last_5_dynamics = []
        asyncio.get_event_loop().run_until_complete(self._async_init())

    async def _async_init(self):
        self.user = await self.get_user_info(self.user_id)

    async def get_json(self, params, url="https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?"):
        async with httpx.AsyncClient() as client:
            r = await client.get(url, params=params, timeout=10.0) # sometimes timeout
            return r.json()

    async def get_user_info(self, user_id):
        url = "https://api.bilibili.com/x/space/acc/info?"
        params = {
            "mid": "378996",
            "jsonp": "jsonp"
        }
        json = await self.get_json(params, url)
        user = {}
        user["id"] = json["data"]["mid"]
        user["screen_name"] = json["data"]["name"]
        return user

    def get_user_id(self):
        return self.user_id
    def get_username(self):
        return self.user["screen_name"]

    def get_text(self, card, dtype):
        if dtype == 2:
            return card["item"]["description"]
        elif dtype in [1, 4]:
            return card["item"]["content"]
        elif dtype == 8:
            return card["dynamic"]
        return ""

    def get_pics(self, card, dtype):
        if dtype == 2:
            return [pic["img_src"] for pic in card["item"]["pictures"]]
        elif dtype == 8:
            return [card["pic"]]
        return []

    def get_video_url(self, card, dtype):
        if dtype == 8:
            # How to parse ?
            # Example: bilibili:\\/\\/video\\/925592586\\/?page=1&player_preload=null&player_width=1920&player_height=1080&player_rotate=0
            pass
        return []
    
    def get_origin(self, card, dtype):
        origin = {}
        if dtype == 1:
            raw_origin = json.loads(card["origin"])
            # TODO 长文章转发
            if "item" not in raw_origin:
                return None 
            if "pictures" in raw_origin["item"]:
                rdtype = 2
            else:
                rdtype = 4
            origin["text"] = self.get_text(raw_origin, rdtype)
            origin["pics"] = self.get_pics(raw_origin, rdtype)
        return origin

    
    def get_title(self, card, dtype):
        if dtype in [8, 64]:
            return card["title"]
        return ""

    def print_one_dynamic(self, dynamic):
        try:
            logger.info(u'动态id：%d' % dynamic['id'])
            logger.info(u'动态正文：%s' % dynamic['text'])
            logger.info(u'原始图片url：%s' % dynamic['pics'])
            logger.info(u'内容标题：%s' % dynamic['title'])
        except OSError:
            pass

    def parse_dynamic(self, raw_dynamic):
        dtype = raw_dynamic["desc"]["type"]
        card = json.loads(raw_dynamic["card"])
        if dtype not in parse_type:
            return None

        dynamic = {}

        dynamic["type"] = dtype
        dynamic["id"] = raw_dynamic["desc"]["dynamic_id"]
        dynamic["timestamp"] = raw_dynamic["desc"]["timestamp"]
        dynamic["user_id"] = raw_dynamic["desc"]["user_profile"]["info"]["uid"]
        dynamic["screen_name"] = raw_dynamic["desc"]["user_profile"]["info"]["uname"]
        
        dynamic["text"] = self.get_text(card, dtype)
        dynamic["pics"] = self.get_pics(card, dtype)
        dynamic["video_url"] = self.get_video_url(card, dtype)
        dynamic["title"] = self.get_title(card, dtype)
        dynamic["retweet"] = self.get_origin(card, dtype)
        if dynamic["retweet"] == None:
            return None # TODO 长文章转发处理
        return dynamic

    def is_recent(self, timestamp):
        now = time.time()
        if (now - timestamp) / 60 / 60 < 48:
            return True
        return False

    async def get_dynamics_by_offset(self, offset, need_top=0):
        params = {
            "visitor_uid":"0",
            "host_uid": self.user_id,
            "offset_dynamic_id": offset,
            "need_top": "0"
        }
        return await self.get_json(params)

    async def get_latest_dynamics(self):
        try:
            latest_dynamics = []
            json = await self.get_dynamics_by_offset(0)

            raw_dynamics = json['data']['cards']
            for raw_dynamic in raw_dynamics:
                logger.info(raw_dynamic)
                dynamic = self.parse_dynamic(raw_dynamic)
                if dynamic != None and self.is_recent(dynamic["timestamp"]):
                    self.print_one_dynamic(dynamic)
                    latest_dynamics.append(dynamic)

                    if len(self.last_5_dynamics) == 5:
                        self.last_5_dynamics.pop(0)
                    self.last_5_dynamics.append(dynamic)
                    self.received_dynamic_ids.append(dynamic["id"])
            return latest_dynamics
        except Exception as e:
            logger.exception(e)
            return []

    def get_last_5_dynamics(self):
        return self.last_5_dynamics

    def clear_buffer(self):
        self.received_dynamic_ids.clear()



