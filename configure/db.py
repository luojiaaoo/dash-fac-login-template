#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : sharingpannel-dev 
@File    : db.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-22 11:09 
'''
import os
from os.path import join
from playhouse.db_url import connect
from configure import BASE_PATH
from configure.mode import LAUNCH_MODE
from playhouse.shortcuts import ReconnectMixin
from peewee import MySQLDatabase

if LAUNCH_MODE == 'dev':
    if not os.path.exists(join(BASE_PATH, 'demo')):
        os.mkdir(join(BASE_PATH, 'demo'))
    db = connect(f"sqlite:///{join(BASE_PATH, 'demo', 'peewee_test.db')}")

