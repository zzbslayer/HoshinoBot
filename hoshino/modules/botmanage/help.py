from hoshino import Service, priv
from hoshino.typing import CQEvent
import itertools

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

HELP_HEADER='''
=====================
- HoshinoBot使用说明 -
=====================
发送方括号[]内的关键词即可触发
※功能采取模块化管理，群管理可控制开关
'''.strip()
HELP_BOTTOM='''
※※该bot是基于HoshinoBot开发的分支版本KokkoroBot
※※调教时请注意使用频率，您的滥用可能会导致bot账号被封禁
'''.strip()

PRC_HELP = '''
==================
- 公主连接Re:Dive -
==================
[/十连] 十连转蛋模拟
[/单抽] 单抽转蛋模拟
[/井] 4w5钻！买定离手！
[查看卡池] 模拟卡池&出率
[切换卡池] 更换模拟卡池
[@bot 妈] 给主さま盖章章
[查看卡池] 查看bot现在的卡池及出率
[怎么拆 妹弓] 后以空格隔开接角色名，查询竞技场解法
[pcr速查] 常用网址/速查表
[bcr速查] B服萌新攻略
[rank表] 查看rank推荐表
[黄骑充电表] 查询黄骑1动充电规律
[@bot 官漫132] 官方四格阅览
[挖矿 15001] 查询矿场中还剩多少钻
[刷图 10] 查看指定地图刷图攻略
[！帮助] 查看会战管理功能的说明
[国服日程表] 查看国服活动日程表
[国服新闻] 查看国服新闻
[国服活动] 查看国服活动安排
[本地化笔记] 查看国服本地化笔记
[启用/禁用 pcr-arena-reminder-cn] 背刺时间提醒(UTC+8)
[启用/禁用 pcr-portion-reminder-cn] 提醒买药小助手(UTC+8)
[启用/禁用 weibo-pcr] 国服官微推送
'''.strip()

ARKNIGHTS_HELP='''
=====================
- 明日方舟 Arknights -
=====================
[公开招募 位移 近战位] 公开招募模拟器
[公招TAG] 公开招募TAG一览
[启用/禁用 weibo-ark] 国服官微推送
'''.strip()

WEIBO_HELP='''
===========
- 微博推送 -
===========
[微博配置] 查看微博推送服务的配置
[@bot 看微博 公主连结] 根据别名查看指定微博账户的最新五条微博
'''.strip()

NORMAL_HELP='''
===========
- 通用功能 -
===========
[切噜一下] 后以空格隔开接想要转换为切噜语的话
[切噜～♪切啰巴切拉切蹦切蹦] 切噜语翻译
[启用/禁用 antiqks] 识破骑空士的阴谋
[启用/禁用 bangumi] 开启番剧更新推送
[@bot 来点新番] 查看最近的更新(↑需先开启番剧更新推送↑)
[.r] 掷骰子
[.r 3d12] 掷3次12面骰子
[@bot 精致睡眠] 8小时精致睡眠(bot需具有群管理权限)
[给我来一份精致昏睡下午茶套餐] 叫一杯先辈特调红茶(bot需具有群管理权限)
[@bot 来杯咖啡] 联系维护组，空格后接反馈内容
'''.strip()

ADMIN_HELP='''
=================
- 群管理限定功能 -
=================
[翻译 もう一度、キミとつながる物語] 机器翻译
[lssv] 查看功能模块的开关状态
'''.strip()

SHORT_HELP=f'''
{HELP_HEADER}
====================
[公主连结帮助]查看公主连结相关功能
[！帮助] 查看公主连结会战管理功能的说明
[明日方舟帮助]查看明日方舟相关功能
[微博帮助]查看微博功能
[通用功能]查看通用功能
[管理员帮助]查看管理员限定功能
====================
{HELP_BOTTOM}
'''.strip()

def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)

_pcr=['公主连结', '公主链接', '公主连接', 'pcr']
_help=['帮助', 'help']
@sv.on_fullmatch(tuple([''.join(l) for l in itertools.product(_pcr, _help)]))
async def pcr_help(bot, ev:CQEvent):
    await bot.send(ev, PRC_HELP)

_ark=['明日方舟', '舟游', 'arknights']
@sv.on_fullmatch(tuple([''.join(l) for l in itertools.product(_ark, _help)]))
async def ark_help(bot, ev:CQEvent):
    await bot.send(ev, ARKNIGHTS_HELP)

_weibo=['wb', '微博', 'weibo']
@sv.on_fullmatch(tuple([''.join(l) for l in itertools.product(_weibo, _help)]))
async def weibo_help(bot, ev:CQEvent):
    await bot.send(ev, WEIBO_HELP)

@sv.on_fullmatch(('通用功能', '通用帮助'))
async def normal_help(bot, ev:CQEvent):
    await bot.send(ev, NORMAL_HELP)

_admin=['admin', '管理员', '管理', '管理限定', '管理员限定']
@sv.on_fullmatch(tuple([''.join(l) for l in itertools.product(_admin, _help)]))
async def weibo_help(bot, ev:CQEvent):
    await bot.send(ev, ADMIN_HELP)

@sv.on_prefix(('help', '帮助', '幫助'))
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        await bot.send(ev, TOP_MANUAL)
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
    else:
        msg = SHORT_HELP
    await bot.send(ev, msg)
