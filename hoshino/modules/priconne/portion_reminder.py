from hoshino.service import Service
from hoshino import R

svcn = Service('pcr-portion-reminder-cn', enable_on_default=False, help_='药水购买小助手（国服）', bundle='pcr订阅')
#msg = "骑士君记得买经验药水哦~"
img = R.img('提醒药水小助手.jpg').cqcode
msg = f'{img}'

@svcn.scheduled_job('cron', hour='0,6,12,18')
async def pcr_portion_reminder_cn():
    print("Portion reminder triggered")
    print(img)
    await svcn.broadcast(msg, 'pcr-portion-reminder-cn')