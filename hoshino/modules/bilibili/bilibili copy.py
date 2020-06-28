import httpx
import json
import time
import asyncio
from hoshino import logger
from hoshino.res import R

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
'''

parse_type = [1, 2, 4, 8]

class BilibiliSpider(object):
    def __init__(self, config):
        self.last_time_gap = 30*60 # 30 min 之前的消息忽略
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

    def parse_dynamic(self, raw_dynamic):
        content_list = []
        try:
            if raw_dynamic['desc']['type'] == 64:
                dynamic['title'] = 
                content_list.append(self.get_username() +'发了新专栏「'+ raw_dynamic['card']['title'] + '」：\n' + raw_dynamic['card']['dynamic'])
            elif: raw_dynamic['desc']['type'] == 8:
                content_list.append(self.get_username() + '发了新视频「'+ raw_dynamic['card']['title'] + '」：\n' + raw_dynamic['card']['dynamic'])
            elif 'description' in cards_data[index]['card']['item']:
                #这个是带图新动态
                content_list.append(self.get_username() + '发了新动态： ' + raw_dynamic['card']['item']['description'] + '\n')
                for pic_info in cards_data[index]['card']['item']['pictures']:
                    content_list.append(R.remote_img(pic_info['img_src']).cqcode)
            else:
                #这个表示转发，原动态的信息在 cards-item-origin里面。里面又是一个超级长的字符串……
                #origin = json.loads(cards_data[index]['card']['item']['origin'],encoding='gb2312') 我也不知道这能不能解析，没试过
                #origin_name = 'Fuck'
                if 'origin_user' in raw_dynamic['card']:
                    origin_name = raw_dynamic['card']['origin_user']['info']['uname']
                    content_list.append(self.get_username()+ '转发了「'+ origin_name + '」的动态并说： ' + raw_dynamic['card']['item']['content'])
                else:
                    #这个是不带图的自己发的动态
                    content_list.append(self.get_username()+ '发了新动态：\n' + raw_dynamic['card']['item']['content'])
            content_list.append('本条动态地址为'+'https://t.bilibili.com/'+ raw_dynamic['desc']['dynamic_id_str'])
        except Exception as err:
            content_list = ["动态解析出了点错误┭┮﹏┭┮"]
            logger.exception(err)

        return content_list, raw_dynamic['desc']['dynamic_id_str']

    def is_recent(self, timestamp):
        now = time.time()
        if now - timestamp < self.last_time_gap:
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
                content_list, did = self.parse_dynamic(raw_dynamic)
                if did in self.received_dynamic_ids:
                    continue
                if content_list == []:
                    continue
                if not self.is_recent(raw_dynamic['desc']['timestamp']):
                    continue
                logger.info(content_list)
                latest_dynamics.append(dynamic)

                if len(self.last_5_dynamics) == 5:
                    self.last_5_dynamics.pop(0)
                self.last_5_dynamics.append(dynamic)
                self.received_dynamic_ids.append(did)
            return latest_dynamics
        except Exception as e:
            logger.exception(e)
            return []

    def get_last_5_dynamics(self):
        return self.last_5_dynamics

    def clear_buffer(self):
        self.received_dynamic_ids.clear()



