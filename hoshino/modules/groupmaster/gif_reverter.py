
# This part is from https://github.com/sahuang/DragonBot-ReDive/tree/master/dragon/plugins/image_revert
# Thanks for @sahuang
from nonebot import on_command, CommandSession, get_bot

from os import listdir, path, stat, makedirs
from random import choice, randint
from string import ascii_letters
import sys
import time
import math

from PIL import Image, ImageSequence
import PIL
from aiocqhttp.message import Message
import httpx
import io
from hoshino import Service, R
from hoshino.util import FreqLimiter

lmt = FreqLimiter(5)

BASE_DIR = R.img('temp/gifs/').path
makedirs(BASE_DIR, exist_ok=True)

sv = Service('gif-reverter', enable_on_default=False)

async def get_image(url, **kwargs):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, **kwargs)
        return r

async def reverse_image(base: str) -> str:
    # get base image
    response = await get_image(base)
    im = Image.open(io.BytesIO(response.content))

    frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
    frames.reverse()

    # save image
    rand_name = ''.join(choice(ascii_letters) for i in range(10)) + '.gif'
    dst = path.join(BASE_DIR, rand_name)
    frames[0].save(dst, save_all=True, append_images=frames[1:], transparency=255, disposal=2)

    tot_size = stat(dst).st_size // 1024
    img = R.img(f'temp/gifs/{rand_name}')

    if tot_size > 1500:
        # needs resize to < 1.5MB
        resize_factor = math.sqrt(tot_size / 1500.)

        size = int(frames[0].size[0] / resize_factor), int(frames[0].size[1] / resize_factor)

        # Wrap on-the-fly thumbnail generator
        def thumbnails(frames):
            for frame in frames:
                thumbnail = frame.copy()
                thumbnail.thumbnail(size)
                yield thumbnail

        frames = thumbnails(frames)
        # Save output
        rand_name = ''.join(choice(ascii_letters) for i in range(10)) + '.gif'
        om = next(frames) # Handle first frame separately
        om.info = im.info # Copy sequence info
        duration_new = 0
        om.save(dst, save_all=True, append_images=list(frames), transparency=255, disposal=2)
    
    return img

@sv.on_prefix(('reverse','倒放', '倒'))
async def reverse(bot, ev):
    msg_without_prefix = ev['message']
    imglist = [ s.data['url'] 
        for s in Message(msg_without_prefix)
        if s.type == 'image' and 'url' in s.data
    ]

    if 'gif' not in msg_without_prefix or len(imglist) == 0:
        bot.finish(ev, '请发送 gif 图片')

    gif = imglist[0]
    
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.finish(ev, f'冷却中(剩余 {int(lmt.left_time(uid)) + 1}秒)')
    
    lmt.start_cd(uid, 120)
    # 向用户发送图
    reverted = await reverse_image(gif)
    await bot.finish(ev, reverted.cqcode)