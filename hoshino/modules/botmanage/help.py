from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
=====================
- HoshinoBot使用说明 -
=====================
发送方括号[]内的关键词即可触发
※功能采取模块化管理，群管理可控制开关
==================
- 公主连接Re:Dive -
==================
[/十连] 十连转蛋模拟
[/单抽] 单抽转蛋模拟
[/井] 4w5钻！买定离手！
[@bot 妈] 给主さま盖章章
[查看卡池] 查看bot现在的卡池及出率
[怎么拆 妹弓] 后以空格隔开接角色名，查询竞技场解法
[pcr速查] 常用网址/速查表
[bcr速查] B服萌新攻略
[rank表] 查看rank推荐表
[黄骑充电表] 查询黄骑1动充电规律
[@bot 官漫132] 官方四格阅览
[启用/禁用 pcr-arena-reminder-jp] 背刺时间提醒(UTC+9)
[启用/禁用 pcr-arena-reminder-cn] 背刺时间提醒(UTC+8)
[启用/禁用 pcr-portion-reminder-cn] 提醒买药小助手(UTC+8)
[启用/禁用 weibo-pcr] 国服官微推送
[挖矿 15001] 查询矿场中还剩多少钻
[切噜一下] 后以空格隔开接想要转换为切噜语的话
[切噜～♪切啰巴切拉切蹦切蹦] 切噜语翻译
[刷图 10] 查看指定地图刷图攻略
[！帮助] 查看会战管理功能的说明
[国服日程表] 查看国服活动日程表
[国服新闻] 查看国服新闻
[国服活动] 查看国服活动安排
[本地化笔记] 查看国服本地化笔记
=====================
- 明日方舟 Arknights -
=====================
[公开招募 位移 近战位] 公开招募模拟器
[公招TAG] 公开招募TAG一览
[启用/禁用 weibo-ark] 国服官微推送
===========
- 微博推送 -
===========
[微博配置] 查看微博推送服务的配置
[@bot 看微博 公主连结] 根据别名查看指定微博账户的最新五条微博
===========
- 通用功能 -
===========
[启用/禁用 antiqks] 自动检测骑空士的陷阱
[启用/禁用 bangumi] 开启番剧更新推送
[@bot 来点新番] 查看最近的更新(↑需先开启番剧更新推送↑)
[.r] 掷骰子
[.r 3d12] 掷3次12面骰子
[@bot 精致睡眠] 8小时精致睡眠(bot需具有群管理权限)
[给我来一份精致昏睡下午茶套餐] 叫一杯先辈特调红茶(bot需具有群管理权限)
[@bot 来杯咖啡] 联系维护组，空格后接反馈内容
=================
- 群管理限定功能 -
=================
[翻译 もう一度、キミとつながる物語] 机器翻译
[lssv] 查看功能模块的开关状态
=======
[!帮助] 会战管理功能说明
[怎么拆日和] 竞技场查询
[星乃来发十连] 转蛋模拟
[pcr速查] 常用网址
[官漫132] 四格漫画（日）
[切噜一下] 切噜语转换
[lssv] 查看功能模块的开关状态（群管理限定）
[来杯咖啡] 联系维护组

发送以下关键词查看更多：
[帮助pcr查询]
[帮助pcr娱乐]
[帮助pcr订阅]
[帮助kancolle]
[帮助通用]
========
※除这里中写明外 另有其他隐藏功能:)
※隐藏功能属于赠品 不保证可用性
※本bot开源，可自行搭建
※服务器运行及开发维护需要成本，赞助支持请私戳作者
※您的支持是本bot更新维护的动力
※※调教时请注意使用频率，您的滥用可能会导致bot账号被封禁
'''.strip()

# @sv.on_fullmatch(('help', 'manual', '帮助', '说明', '使用说明', '幫助', '說明', '使用說明', '菜单', '菜單'))
# async def send_help(bot, ev: CQEvent):
#     await bot.send(ev, MANUAL)


def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'o' if sv.check_enabled(gid) else 'x'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)


@sv.on_prefix(('help', '帮助', '幫助'))
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
    else:
        msg = TOP_MANUAL
    await bot.send(ev, msg)
