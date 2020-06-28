from .bilibili import BilibiliSpider
from hoshino.service import Service, priv as Priv
from hoshino.res import R
from hoshino import util
from .exception import *

'''
sample config.json
[{
    "service_name": "bcr-bilibili",
    "enable_on_default": true,
    "users":[{
        "user_id": "6603867494",
        "alias": ["公主连接", "公主连结", "公主链接"],
    }]
    
}]
'''
def _load_config(services_config):
    for sv_config in services_config:
        sv.logger.debug(sv_config)
        service_name = sv_config["service_name"]
        enable_on_default = sv_config.get("enable_on_default", False)

        users_config = sv_config["users"]

        sv_spider_list = []
        for user_config in users_config:
            bili_spider = BilibiliSpider(user_config)
            sv_spider_list.append(bili_spider)
            alias_list = user_config.get("alias", [])
            for alias in alias_list:
                if alias in alias_dic:
                    raise DuplicateError(f"Alias {alias} is duplicate")
                alias_dic[alias] = {
                    "service_name":service_name, 
                    "user_id":bili_spider.get_user_id()
                    }

        subService = Service(service_name, enable_on_default=enable_on_default)
        subr_dic[service_name] = {"service": subService, "spiders": sv_spider_list}



sv = Service('bilibili-poller', use_priv=Priv.ADMIN, manage_priv=Priv.SUPERUSER, visible=False)
services_config = util.load_config(__file__)
subr_dic = {}
alias_dic = {}
_load_config(services_config)

def dynamic_to_message(dynamic):
    msg = f'@{dynamic["screen_name"]}'
    if "retweet" in dynamic:
        msg = f'{msg} 转发:\n{dynamic["text"]}\n======================'
        dynamic = dynamic["retweet"]
    else:
        msg = f'{msg}:'

    msg = f'{msg}\n{dynamic["text"]}'

    if dynamic["title"] != "":
        msg = f'{msg}\n{dynamic["title"]}'
    if sv.bot.config.IS_CQPRO and len(dynamic["pics"]) > 0:
        images_url = dynamic["pics"]
        msg = f'{msg}\n'
        res_imgs = [R.remote_img(url).cqcode for url in images_url]
        for img in res_imgs:
            msg = f'{msg}{img}'
    if len(dynamic["video_url"]) > 0:
        videos = dynamic["video_url"]
        res_videos = ';'.join(videos)
        msg = f'{msg}\n视频链接：{res_videos}'
    return msg

# @bot 看微博 alias
@sv.on_command('看b博', only_to_me=True)
async def get_last_5_dynamics(session):
    alias = session.current_arg_text
    if alias not in alias_dic:
        await session.finish(f"未找到 bilibili 用户: {alias}")
        return
    service_name = alias_dic[alias]["service_name"]
    user_id = alias_dic[alias]["user_id"]

    spiders = subr_dic[service_name]["spiders"]
    for spider in spiders:
        if spider.get_user_id() == user_id:
            last_5_dynamics = spider.get_last_5_dynamics()
            formatted_dynamics = [dynamic_to_message(dynamic) for dynamic in last_5_dynamics]
            for dynamic in formatted_dynamics:
                await session.send(dynamic)
            await session.finish(f"以上为 {alias} 的最新 {len(formatted_dynamics)} 条 bilibili 动态")
            return
    await session.finish(f"未找到 bilibili 用户: {alias}")

@sv.scheduled_job('interval', seconds=20)
async def bilibili_poller():
    for sv_name, serviceObj in subr_dic.items():
        dynamics = []
        ssv = serviceObj["service"]
        spiders = serviceObj["spiders"]
        for spider in spiders:
            latest_dynamics = await spider.get_latest_dynamics()
            formatted_dynamics = [dynamic_to_message(dynamic) for dynamic in latest_dynamics]

            if l := len(formatted_dynamics):
                sv.logger.info(f"成功获取@{spider.get_username()}的新动态{l}条")
            else:
                sv.logger.info(f"未检测到@{spider.get_username()}的新动态")

            dynamics.extend(formatted_dynamics)
        await ssv.broadcast(dynamics, ssv.name, 0.5)

@sv.scheduled_job('interval', seconds=60*60*24)
async def clear_spider_buffer():
    sv.logger.info("Clearing weibo spider buffer...")
    for sv_name, serviceObj in subr_dic.items():
        spiders = serviceObj["spiders"]
        for spider in spiders:
            spider.clear_buffer() 
