#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : main.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-18 13:11 
'''
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.__str__())
from app import app
from server import server
# 定义日志输出
import common.log
# 引入huey调度框架
from server import huey
from task import tasks

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
