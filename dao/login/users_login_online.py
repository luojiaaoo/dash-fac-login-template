#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : users_online.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-11 11:56 
'''

from configure.db import db
from peewee import Model, CharField, DateTimeField, DoesNotExist
import datetime


class UsersLoginOnline(Model):
    name = CharField(max_length=32, unique=True)
    ip = CharField(max_length=16)
    session_id = CharField(max_length=50)
    login_time = DateTimeField()
    last_active_time = DateTimeField()

    class Meta:
        database = db
        table_name = 'users_login_online'


def insert_login_online(name, session_id, ip):
    now = datetime.datetime.now()
    try:
        u = UsersLoginOnline.get(UsersLoginOnline.name == name)
    except DoesNotExist:
        UsersLoginOnline.insert(name=name, session_id=session_id, ip=ip, login_time=now, last_active_time=now).execute()
    else:
        if u.session_id != session_id:
            with db.atomic() as txn:
                from ..login.users_login_hist import UsersLoginHist
                u_old = UsersLoginOnline.get(
                    UsersLoginOnline.name == name and
                    UsersLoginOnline.session_id == u.session_id
                )
                UsersLoginHist.insert(
                    login_time=u_old.login_time,
                    logout_time=u_old.last_active_time,
                    name=u_old.name,
                    ip=u_old.ip
                ).execute()
                UsersLoginOnline.delete().where(
                    UsersLoginOnline.name == name and
                    UsersLoginOnline.session_id == u_old.session_id
                ).execute()
                UsersLoginOnline.insert(
                    name=name,
                    session_id=session_id,
                    login_time=now,
                    last_active_time=now,
                    ip=ip
                ).execute()


def is_online(name, session_id, ip):
    try:
        UsersLoginOnline.get(
            UsersLoginOnline.name == name and
            UsersLoginOnline.session_id == session_id
        )
    except DoesNotExist:
        return False
    else:
        UsersLoginOnline.update(
            {
                UsersLoginOnline.last_active_time: datetime.datetime.now(),
                UsersLoginOnline.ip: ip
            }
        ).where(
            UsersLoginOnline.name == name,
            UsersLoginOnline.session_id == session_id
        ).execute()
        return True


def clear_online_active_timeout():
    us = UsersLoginOnline.select().where(
        UsersLoginOnline.last_active_time < datetime.datetime.now() - datetime.timedelta(minutes=5)
    )
    for u in us:
        pop_online(u.name, u.session_id)


def pop_online(name, session_id):
    from ..login.users_login_hist import UsersLoginHist
    try:
        u = UsersLoginOnline.get(
            UsersLoginOnline.name == name and
            UsersLoginOnline.session_id == session_id
        )
    except DoesNotExist:
        ...
    else:
        with db.atomic() as txn:
            UsersLoginHist.insert(
                login_time=u.login_time,
                logout_time=u.last_active_time,
                name=u.name,
                ip=u.ip
            ).execute()
            UsersLoginOnline.delete().where(
                UsersLoginOnline.name == name and
                UsersLoginOnline.session_id == session_id
            ).execute()
