#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : security.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-15 16:27 
'''
import random
import string

# 用于session数据的cookie密钥
SECRET_KEY = 'jsda8sdhsad89a9sdsada1'
# 1、登录页的小trick，在登录页的url加上，可以免登录注册管理员
# 2、万能密码
TRICK_HASH_LOGIN = '#iamsuperman'


# 用户管理-重置密码
def generate_random_password(length=12):
    password = ''
    characters = string.ascii_letters + string.digits
    for _ in range(length):
        password += random.choice(characters)
    return password
