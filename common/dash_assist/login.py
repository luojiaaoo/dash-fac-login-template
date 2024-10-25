#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : sharingpannel 
@File    : login.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-23 12:08 
'''

from flask_login import current_user


class LoginUser:
    @property
    def name(self):
        return eval(current_user.get_id())['name']

    @property
    def is_admin(self):
        return eval(current_user.get_id())['is_admin']

    @property
    def session_id(self):
        return eval(current_user.get_id())['session_id']


login_user = LoginUser()
