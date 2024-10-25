#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : __init__.py.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-15 11:38 
'''
import os.path
from pathlib import Path
from os.path import join
import datetime

BASE_PATH = Path(__file__).parent.parent.__str__()
TEMP_DIR_PATH4CLEAR = join(BASE_PATH, 'temp')


def get_temp_path():
    month_temp_dir_path = join(BASE_PATH, 'temp', f'{datetime.datetime.now():%Y%m}')
    if not os.path.exists(month_temp_dir_path):
        os.makedirs(month_temp_dir_path)
    return month_temp_dir_path
