
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
import requests
import io
from hoshino import Service, R

BASE_DIR = R.img('temp/gifs/').path
makedirs(BASE_DIR, exist_ok=True)

sv = Service('gif-reverter', enable_on_default=False)

async def reverse_image(base: str) -> str:

    # get base image
    response = requests.get(base)
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

@sv.on_command('reverse', aliases=('倒放', '倒'), only_to_me=False)
async def reverse(session: CommandSession):

    # 从会话状态中获取图片
    base = session.get('base', prompt='请向机器人发送gif。')

    # 向用户发送图
    reverted = await reverse_image(base)
    await session.send(reverted.cqcode)

@reverse.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        # 该命令第一次运行arg
        if 'CQ:image' in arg and 'gif' in arg:
            session.state['base'] = session.current_arg_images[0]
        return

    if session.current_key == 'base':
        if 'CQ:image' in arg and 'gif' in arg:
            session.state['base'] = session.current_arg_images[0]
        else:
            session.finish('请发送gif。')