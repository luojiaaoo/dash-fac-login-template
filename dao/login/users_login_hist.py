#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : users_hist.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-11 11:56 
'''

from configure.db import db
from peewee import Model, CharField, DateTimeField


class UsersLoginHist(Model):
    login_time = DateTimeField()
    logout_time = DateTimeField()
    name = CharField(max_length=32)
    ip = CharField(max_length=16)

    class Meta:
        database = db
        table_name = 'users_login_hist'
