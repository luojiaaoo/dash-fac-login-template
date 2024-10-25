#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : huey.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-18 11:42 
'''
import datetime
import os
import time

from huey import crontab
from server import huey


# 动态注册
@huey.task()
def schedule_message(message, cron_minutes, cron_hours='*'):
    '''
    schedule_message('I run every 5 minutes', '*/5')
    schedule_message('I run between 0-15 and 30-45', '0-15,30-45')
    '''

    def wrapper():
        print('dynamically-created periodic task: "%s"' % message)

    schedule = crontab(cron_minutes, cron_hours)
    task_name = 'dynamic_ptask_%s' % int(time.time())
    huey.periodic_task(schedule, name=task_name)(wrapper)


@huey.periodic_task(crontab(minute='*/5'))
def every_five_minutes():
    from dao.login.users_login_online import clear_online_active_timeout
    clear_online_active_timeout()


@huey.periodic_task(crontab(minute='0', hour='3'))
def clear_temp():
    import re
    import shutil
    from configure import TEMP_DIR_PATH4CLEAR
    for i in os.listdir(TEMP_DIR_PATH4CLEAR):
        if re.match(r'\d{6}', i) and i <= f'{datetime.datetime.now() - datetime.timedelta(days=30):%Y%m}':
            shutil.rmtree(i)
