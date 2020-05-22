from hoshino import Service, Privilege

sv = Service('gfw-help', manage_priv=Privilege.SUPERUSER, enable_on_default=False, visible=False)
help_message = '''
=====================
-      使用说明      -
=====================
输入方括号[]内的关键词即可触发相应的功能
※部分功能必须手动at本bot才会触发(复制无效)
=====================
-      General      -
=====================
[演唱会帮助] 演唱会使用说明
[演唱会模式] 演唱会模式说明
[演唱会门票] 演唱会门票说明
[演唱会地址刷新] 如何刷新演唱会地址
=====================
-     v2 演唱会      -
=====================
[v2-how] 如何参与 v2 演唱会
[v2-download] v2 演唱会门票下载
[v2-config] v2 演唱会门票配置信息
'''

help_aliases=('演唱会帮助', '演唱会说明', '演唱会help', '演唱会 help')
@sv.on_command('gfw-help', aliases=help_aliases)
async def gfw_help(session):
    await session.send(help_message)

mode_aliases=('演唱会模式', '演唱会mode', '演唱会 mode')
@sv.on_command('proxy-mode', aliases=mode_aliases)
async def mode_help(session):
    msg = '演唱会模式'
    msg = f'{msg}\n全局：全部歌曲从演唱会听'
    msg = f'{msg}\nPAC：特定歌曲从演唱会听'
    msg = f'{msg}\n直连：不从演唱会听歌'
    await session.send(msg)

tickets = ('ss', 'v2')
mode_aliases=('演唱会门票')
@sv.on_command('proxy-client', aliases=mode_aliases)
async def mode_help(session):
    msg = '演唱会门票十元每月，喜欢的粉丝们可以酌情打赏'
    msg = f'{msg}\n目前支持 {tickets}'
    await session.send(msg)

dns_aliases=('演唱会地址刷新')
@sv.on_command('flush-dns', aliases=dns_aliases)
async def dns_help(session):
    msg = '在命令行中执行以下命令：'
    msg = f'{msg}\nwindows: ipconfig /flushdns'
    msg = f'{msg}\nmac OSX: sudo dscacheutil -flushcache'
    msg = f'{msg}\n本群已与百度达成合作协议，如果找不到您的系统，可以去百度搜索！'
    await session.send(msg)