from hoshino import Service

sv = Service('pcr-calendar')
cn_official_url = 'https://wiki.biligame.com/pcr/%E6%B4%BB%E5%8A%A8%E6%97%A5%E5%8E%86'
@sv.on_rex(r'^\*?([日台国bB])服?(日历|日程|日程表)?$')
async def calendar(bot, ev):
    match = ev.match
    server = match.group(1)
    if server == '台':
        await bot.send(ev, "不好意思，台服日程表暂不支持┭┮﹏┭┮", at_sender=True)
        return
    elif server == '日':
        region = 'jp'
    elif server in ['国', 'b', 'B']:
        region = 'cn'

    yobot_url = f'https://tools.yobot.win/calender/#{region}'
    msg = f'{server}服日程表\nyobot: {yobot_url}'
    if region == 'cn':
        msg = f'{msg}\nbilibili: {cn_official_url}'
    await bot.send(ev, msg)