import random

from nonebot import on_command

from hoshino import R, Service, priv, util


# basic function for debug, not included in Service('chat')
@on_command('zai?', aliases=('在?', '在？', '在吗', '在么？', '在嘛', '在嘛？'), only_to_me=True)
async def say_hello(session):
    await session.send('はい！私はいつも貴方の側にいますよ！')


sv = Service('chat', manage_priv=priv.SUPERUSER, visible=False)


@sv.on_fullmatch(('沙雕机器人', '沙雕機器人'))
async def say_sorry(bot, ev):
    await bot.send(ev, 'ごめんなさい！嘤嘤嘤(〒︿〒)')


@sv.on_fullmatch(('老婆', 'waifu', 'laopo'), only_to_me=True)
async def chat_waifu(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, R.img('laopo.jpg').cqcode)
    else:
        await bot.send(ev, 'mua~')


@sv.on_fullmatch('老公', only_to_me=True)
async def chat_laogong(bot, ev):
    await bot.send(ev, '你给我滚！', at_sender=True)


@sv.on_fullmatch('mua', only_to_me=True)
async def chat_mua(bot, ev):
    await bot.send(ev, '笨蛋~', at_sender=True)


@sv.on_fullmatch('来点星奏')
async def seina(bot, ev):
    await bot.send(ev, R.img('星奏.png').cqcode)

@sv.on_fullmatch(('我有个朋友说他好了', '我朋友说他好了', ))
async def ddhaole(bot, ev):
    await bot.send(ev, '那个朋友是不是你弟弟？')

@sv.on_fullmatch('我好了')
async def nihaole(bot, ev):
    await bot.send(ev, '不许好，憋回去！')

# ============================================ #


@sv.on_keyword(('确实', '有一说一', 'u1s1', 'yysy'))
async def chat_queshi(bot, ctx):
    if random.random() < 0.05:
        await bot.send(ctx, R.img('确实.jpg').cqcode)


@sv.on_keyword(('会战'))
async def chat_clanba(bot, ctx):
    if random.random() < 0.02:
        await bot.send(ctx, R.img('我的天啊你看看都几度了.jpg').cqcode)

def possibilities(pos, cnt):
    return [pos * (i+1) / cnt for i in range(cnt)]

ng_pos = 0.20
neigui = ['内鬼.png', '内鬼-1.jpg', '内鬼-2.jpg']
ng_poses = possibilities(ng_pos, len(neigui))

@sv.on_keyword(('内鬼'))
async def chat_neigui(bot, ctx):
    r = random.random()
    cnt = len(neigui)

    if  r < ng_pos:
        for i in range(cnt):
            if r < ng_poses[i]:
                await bot.send(ctx, R.img(neigui[i]).cqcode)
                return

@sv.on_keyword(('非酋', '非洲', '脸黑'))
async def africa(bot, ctx):
    cmd = ev.message.extract_plain_text().strip()
    if random.random() < 0.2:
        await bot.send(ctx, R.img('非酋.png').cqcode)

nyb_player = f'''{R.img('newyearburst.gif').cqcode}
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''.strip()

@sv.on_keyword(('春黑', '新黑'))
async def new_year_burst(bot, ev):
    cmd = ev.message.extract_plain_text().strip()
    if cmd in ['春黑.gif', '新黑.gif'] or random.random() < 0.02:
        await bot.send(ev, nyb_player)
