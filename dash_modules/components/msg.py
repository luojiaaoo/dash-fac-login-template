#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : msg.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-19 22:41 
'''

from dash.dependencies import Output, Input
import feffery_antd_components.alias as fac


class Components:

    def message(self, content, type, duration=3):
        return fac.Message(
            content=content,
            type=type,
            duration=duration,
        )
