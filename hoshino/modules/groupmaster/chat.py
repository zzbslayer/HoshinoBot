import random, itertools

from nonebot import on_command

from hoshino import R, Service, priv, util


# basic function for debug, not included in Service('chat')
@on_command('zai?', aliases=('在?', '在？', '在吗', '在么？', '在嘛', '在嘛？'), only_to_me=True)
async def say_hello(session):
    await session.send('はい！私はいつも貴方の側にいますよ！')


sv = Service('chat', visible=False)

@sv.on_fullmatch(('沙雕机器人', '沙雕機器人'))
async def say_sorry(bot, ev):
    await bot.send(ev, 'ごめんなさい！嘤嘤嘤(〒︿〒)')


@sv.on_fullmatch(('老婆', 'waifu', 'laopo'), only_to_me=True)
async def chat_waifu(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, R.img('laopo.jpg').cqcode)
    else:
        await bot.send(ev, R.record('要不行了.m4a').cqcode)
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
async def chat_queshi(bot, ev):
    cmd = ev.message.extract_plain_text().strip()
    if cmd in ['确实.jpg'] or random.random() < 0.05:
        await bot.send(ev, R.img('确实.jpg').cqcode)

_audio_suffix = ['.mp3', '.m4a', '.wav']
_yrmsn = ('压力马斯内','yarimasune', 'やりますね')
@sv.on_keyword(tuple(_yrmsn))
async def yarimasune(bot, ev):
    cmd = ev.message.extract_plain_text().strip()
    if cmd in [''.join(l) for l in itertools.product(_yrmsn, _audio_suffix)] or random.random() < 0.05:
        await bot.send(ev, R.record('压力马斯内.m4a').cqcode)

@sv.on_keyword(('会战'))
async def chat_clanba(bot, ev):
    if random.random() < 0.02:
        await bot.send(ev, R.img('我的天啊你看看都几度了.jpg').cqcode)

def possibilities(pos, cnt):
    return [pos * (i+1) / cnt for i in range(cnt)]

_neigui = ['内鬼']
_image_suffix = ['.jpg', '.png']
ng_pos = 0.20
neigui = ['内鬼.png', '内鬼-1.jpg', '内鬼-2.jpg', '内鬼-3.png']
ng_poses = possibilities(ng_pos, len(neigui))
@sv.on_keyword(tuple(_neigui))
async def chat_neigui(bot, ev):
    cmd = ev.message.extract_plain_text().strip()
    r = random.random()
    cnt = len(neigui)
    if cmd in [''.join(l) for l in itertools.product(_neigui, _image_suffix)]:
        random_idx = random.randint(0, cnt - 1)
        img = neigui[random_idx]
    elif  r < ng_pos:
        for i in range(cnt):
            if r < ng_poses[i]:
                img = neigui[i]
                break
    else:
        return
    await bot.send(ev, R.img(img).cqcode)

_africa = ['非酋', '非洲', '脸黑', '非洲人']
africa_pos = 0.05
african = ['非洲人.png','非洲人2.png', '非洲人3.png']
africa_poses = possibilities(africa_pos, len(african))
@sv.on_keyword(tuple(_africa))
async def africa(bot, ev):
    cmd = ev.message.extract_plain_text().strip()
    r = random.random()
    cnt = len(african)
    if cmd in [''.join(l) for l in itertools.product(_africa, _image_suffix)]:
        random_idx = random.randint(0, cnt - 1)
        img = african[random_idx]
    elif  r < africa_pos:
        for i in range(cnt):
            if r < africa_poses[i]:
                img = african[i]
                break
    else:
        return
    await bot.send(ev, R.img(img).cqcode)

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

_ue_sorry = ['ue对不起', '优衣对不起']
@sv.on_keyword(tuple(_ue_sorry))
async def new_year_burst(bot, ev):
    cmd = ev.message.extract_plain_text().strip()
    if cmd in [''.join(l) for l in itertools.product(_ue_sorry, _image_suffix)] or random.random() < 0.02:
        await bot.send(ev, R.img('ue_sorry.jpg').cqcode)
    
@sv.on_keyword(('\\test'))
async def test(bot, ev):
    await bot.send(ev, R.record('test.m4a').cqcode)