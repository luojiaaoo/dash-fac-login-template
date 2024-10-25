#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : log.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-21 19:56 
'''
from dao.log import add_log
from loguru import logger
import datetime
from configure.show import LOGGER_LEVEL

logger.level(LOGGER_LEVEL)


def log_to_db(msg: str):
    msg_split = msg.split('|s|s|')
    time = datetime.datetime.strptime(msg_split[0], '%Y-%m-%d %H:%M:%S')
    level = msg_split[1]
    text = msg_split[2]
    add_log(text=text, level=level, time=time)


logger.add(log_to_db, format="{time:YYYY-MM-DD HH:mm:ss}|s|s|{level}|s|s|{message}")
