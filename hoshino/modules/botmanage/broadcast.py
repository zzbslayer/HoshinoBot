import asyncio

from nonebot import on_command, CommandSession
from nonebot import permission as perm

from hoshino.log import logger
from hoshino import CommandSession, Service, Privilege as Priv

sv = Service('broadcast', use_priv=Priv.SUPERUSER, manage_priv=Priv.SUPERUSER, visible=False)

@on_command('broadcast', aliases=('bc', '广播'), permission=perm.SUPERUSER)
async def broadcast(session:CommandSession):
    msg = session.current_arg
    await sv.admin_broadcast(session, msg, '广播', 0)
    await session.send(f'广播完成！')
