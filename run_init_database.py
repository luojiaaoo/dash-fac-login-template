#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : init_database.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-15 21:50 
'''

import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.__str__())
from configure.db import db
from dao.login.users import Users
from dao.login.users_login_hist import UsersLoginHist
from dao.login.users_login_online import UsersLoginOnline
from dao.log import Log
import datetime
import hashlib

db.connection()
db.create_tables([Users, UsersLoginHist, UsersLoginOnline, Log])
now = datetime.datetime.now()
try:
    Users.insert(name='admin', md5_password=hashlib.md5('admin'.encode()).hexdigest(), is_admin=True, create_time=now,
                 expire_time=now + datetime.timedelta(days=365 * 5)).execute()
except:
    pass
