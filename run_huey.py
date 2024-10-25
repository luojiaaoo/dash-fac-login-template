#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : start_huey.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-18 12:20 
'''
import sys, os
from pathlib import Path

sys.path.append(Path(__file__).parent.__str__())
from configure import BASE_PATH
from os.path import join

os.system(f'{sys.executable} {join(BASE_PATH, "task", "huey_consumer.py")} run_main.huey -w2 -k thread')
