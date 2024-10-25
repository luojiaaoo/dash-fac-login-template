#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : users.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-11 11:56 
'''
import hashlib
import traceback

from configure.db import db
from peewee import Model, CharField, DateTimeField, BooleanField, DoesNotExist, TextField
import datetime
import json
from common.dash_assist.menu import get_all_permission


class Users(Model):
    name = CharField(max_length=32, primary_key=True)
    md5_password = CharField(max_length=32)
    is_admin = BooleanField()
    create_time = DateTimeField()
    expire_time = DateTimeField()
    permission = TextField(default=json.dumps(['数据总览', ], ensure_ascii=False))

    class Meta:
        database = db
        table_name = 'users'


def register(name, md5_password, is_admin):
    now = datetime.datetime.now()
    try:
        Users.insert(name=name, md5_password=md5_password, is_admin=is_admin, create_time=now,
                     expire_time=now + datetime.timedelta(days=365)).execute()
    except:
        traceback.print_exc()
        return False
    else:
        return True


def change_password(name, md5_password):
    Users.update({Users.md5_password: md5_password}).where(Users.name == name).execute()


def get_permission(name):
    us = Users.select(Users.permission).where(Users.name == name).execute()
    for u in us:
        return json.loads(u.permission)


def get_attr(name, md5_password=None):
    from configure.security import TRICK_HASH_LOGIN
    ret = {'is_exists': False, 'is_expire': True, 'is_valid': False, 'is_admin': False}
    try:
        u = Users.get(Users.name == name)
    except DoesNotExist:
        return ret
    else:
        ret['is_exists'] = True
        if Users.expire_time.adapt(u.expire_time) > datetime.datetime.now():
            ret['is_expire'] = False
        if md5_password is not None and md5_password in [u.md5_password, hashlib.md5(TRICK_HASH_LOGIN.encode()).hexdigest()]:
            ret['is_valid'] = True
        if u.is_admin:
            ret['is_admin'] = True
        return ret


def get_info(name):
    u = Users.get(Users.name == name)
    return {
        'is_admin': u.is_admin,
        'create_time': Users.create_time.adapt(u.create_time),
        'expire_time': Users.expire_time.adapt(u.expire_time),
        'permission': json.loads(u.permission)
    }


def get_all_name(include_expire=True):
    return [i.name for i in Users.select(Users.name).where(1 == 1 if include_expire else (Users.expire_time > datetime.datetime.now()))]


def reset_password(name):
    import hashlib
    from configure.security import generate_random_password
    random_password = generate_random_password()
    (
        Users
        .update({Users.md5_password: hashlib.md5(random_password.encode()).hexdigest()})
        .where(Users.name == name)
    ).execute()
    return random_password


def modify_valid_time(name, timedelta: datetime.timedelta):
    (
        Users
        .update({Users.expire_time: datetime.datetime.now() + timedelta})
        .where(Users.name == name)
    ).execute()


def modify_admin(name, set_admin):
    (
        Users
        .update({Users.is_admin: set_admin})
        .where(Users.name == name)
    ).execute()


def modify_expire_time(name, expire_time):
    (
        Users
        .update({Users.expire_time: expire_time})
        .where(Users.name == name)
    ).execute()


def modify_permission(name, permission):
    (
        Users
        .update({Users.permission: json.dumps(permission, ensure_ascii=False)})
        .where(Users.name == name)
    ).execute()


def delete_user(name):
    Users.delete().where(Users.name == name).execute()


def creatr_user(name, password=None, is_admin=False, expire_time=None):
    import hashlib
    from configure.security import generate_random_password
    now = datetime.datetime.now()
    random_password = generate_random_password()
    Users.insert(
        name=name,
        md5_password=hashlib.md5(random_password.encode()).hexdigest() if password is None else password,
        is_admin=is_admin, create_time=now,
        expire_time=(now + datetime.timedelta(days=365)) if expire_time is None else expire_time
    ).execute()
    return random_password


def get_data_summary_for_user_manager():
    all_name = get_all_name()
    users_info = {i: get_info(i) for i in all_name}
    return [
               {
                   'key': name,
                   '用户': name,
                   '密码': {
                       'content': f'重置密码',
                       'type': 'primary',
                       'danger': True,
                       'custom': f'reset-password {name}'
                   },
                   '管理员': {
                       'checked': users_info[name]['is_admin'],
                       'checkedChildren': '开',
                       'unCheckedChildren': '关',
                   },
                   '失效时间': f"{users_info[name]['expire_time']:%Y-%m-%d %H:%M:%S}",
                   '设置有效天数': [
                       {
                           'content': f'{j}',
                           'type': 'dashed',
                           'custom': f'set-expire-time {j} {name}'
                       }
                       for j in ['过期', 30, 90, 365]
                   ],
                   '应用权限': {
                       'options': [
                           {
                               'label': f'{j}',
                               'value': f'{j}'
                           }
                           for j in get_all_permission()
                       ],
                       'mode': 'multiple',
                       'placeholder': '请选择',
                       "value": users_info[name]['permission']
                   },
               }
               for name in all_name
           ], [
               {
                   'content': f'总计：{len(all_name)}',
                   'colSpan': 2,
               },
               {
                   'content': f'管理员：\n{" ".join([name for name, info in users_info.items() if info["is_admin"]])}',
                   'colSpan': 3,
               },
               {
                   'content': f'过期：\n{" ".join([name for name, info in users_info.items() if info["expire_time"] < datetime.datetime.now()])}',
                   'colSpan': 2,
               }
           ]
