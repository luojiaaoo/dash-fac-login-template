#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2
@File    : app.py
@IDE     : PyCharm
@Author  : LUOJA
@Date    : 2024-3-18 13:11
'''
import os
from server import app  # server配置鉴权功能
from flask_login import current_user
from dash_modules.views.enter import login, main
from configure import get_temp_path
from flask import request

if not os.path.exists(get_temp_path()):
    os.mkdir(get_temp_path())


# 添加上传服务
@app.server.route('/upload/', methods=['POST'])
def upload():
    uploadId = request.values.get('uploadId')
    filename = request.files['file'].filename
    try:
        os.mkdir(os.path.join(get_temp_path(), uploadId))
    except FileExistsError:
        pass
    with open(os.path.join(get_temp_path(), uploadId, filename), 'wb') as f:
        for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
            f.write(chunk)
    return {'filename': filename}


# 无登录，自动定义至登录页面
app.layout = lambda: main.render_content() if current_user.is_authenticated else login.render_content()
