from hoshino import Service, Privilege

sv = Service('v2ray-help', manage_priv=Privilege.SUPERUSER, enable_on_default=False, visible=False)

download_prefix = 'http://47.106.8.44/gfw/v2'
windows_download = f'{download_prefix}/v2ray-windows-64.zip'
android_download = f'{download_prefix}/BifrostV.zip'
ios_download = '请在外区商店购买 shadowrocket'
v2download_aliases=('v2download', 'v2raydownload', 'v2下载', 'v2ray下载')
@sv.on_command('v2-download', aliases=v2download_aliases, only_to_me=False)
async def v2download(session):
    msg = '下载地址：'
    msg = f'{msg}\nwindows: {windows_download}'
    msg = f'{msg}\nios: {ios_download}'
    msg = f'{msg}\nandroid: {android_download}'
    msg = f'{msg}\n如果没有您使用的系统，不如问问万能的群友'
    await session.send(msg)

addresses = ['zenyatta.doomfist.xyz', 'ana.doomfist.xyz']
port = 20900
uuid = '034cb94e-7f10-47e8-a020-fca628f0a94a'
v2config_aliases=('v2config', 'v2rayconfig', 'v2配置', 'v2ray配置')
@sv.on_command('v2-config', aliases=v2config_aliases, only_to_me=False)
async def v2download(session):
    msg = '配置方法：'
    msg = f'{msg}\n地址(主机/address): {addresses} （任选一个即可，如果其中某个地址连接有问题，请更换列表中其他地址）'
    msg = f'{msg}\n端口(port): {port}'
    msg = f'{msg}\n用户ID(id/uuid): {uuid}'
    msg = f'{msg}\n其他信息保持默认配置即可'
    await session.send(msg)

v2config_aliases=('v2how', 'v2rayhow')
@sv.on_command('v2-how', aliases=v2config_aliases, only_to_me=False)
async def v2download(session):
    msg = '使用方法：'
    msg = f'{msg}\n1. 下载 v2 客户端'
    msg = f'{msg}\n2. 配置 v2 客户端'
    msg = f'{msg}\n3. 启动 v2'
    msg = f'{msg}\n其他信息保持默认配置即可'
    await session.send(msg)