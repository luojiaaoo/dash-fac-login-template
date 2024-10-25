#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : log.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-21 19:22 
'''

from configure.db import db
from peewee import Model, CharField, DateTimeField, BooleanField, DoesNotExist, TextField
import datetime
from flask_login import current_user
from typing import Optional
from common import login_user


class Log(Model):
    name = CharField(max_length=32, default='unknown')
    level = CharField(max_length=8, default='info')
    time = DateTimeField()
    text = TextField()

    class Meta:
        database = db
        table_name = 'log'


def add_log(text: str, time: datetime.datetime, level: Optional[str] = None):
    try:
        name = login_user.name
    except:
        name = None
    Log(
        **({} if name is None else {'name': name}),
        **({} if level is None else {'level': level}),
        time=time,
        text=text
    ).save()
