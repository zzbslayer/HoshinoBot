import hoshino
from hoshino import R, util, Service
from hoshino.typing import NoticeSession

sv1 = Service('group-leave-notice')
sv2 = Service('group-welcome')

@sv1.on_notice('group_decrease.leave')
async def leave_notice(session: NoticeSession):
    await session.send(f"{session.ctx['user_id']}退群了。")


def gen_msg(msg_list):
    for i in range(len(msg_list)):
        msg = msg_list[i]
        if msg[-3:] in ["png", "jpg", "jpeg"]:
            msg_list[i] = str(R.img(msg).cqcode)
    return '\n'.join(msg_list)

@sv2.on_notice('group_increase')
async def increace_welcome(session: NoticeSession):
    
    if session.event.user_id == session.event.self_id:
        return  # ignore myself
    
    welcomes = hoshino.config.groupmaster.increase_welcome
    gid = session.event.group_id
    if gid in welcomes:
        msg_list = welcomes[gid]
        await session.send(gen_msg(msg_list), at_sender=True)
    elif 'default' in welcomes:
        msg_list = welcomes['default']
        await session.send(gen_msg(msg_list), at_sender=True)
        
