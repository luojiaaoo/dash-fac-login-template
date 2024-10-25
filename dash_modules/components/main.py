#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : main.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-19 21:39 
'''
from dash.dependencies import Output, Input
import feffery_antd_components as fac
from dash import dcc


class Components:

    @property
    def output_main_trigger_reload(self):
        return Output('main-trigger-reload', 'reload', allow_duplicate=True)

    @property
    def input_main_interval_20s(self):
        return Input('main-interval-20s', 'n_intervals')

    @property
    def output_main_message_popup(self):
        return Output('main-message-popup', 'children', allow_duplicate=True)

    @property
    def output_main_download_text(self):
        return Output('main-download-text', 'data', allow_duplicate=True)

    @staticmethod
    def go_login(note):
        return fac.AntdParagraph(
            [
                f'{note}，',
                dcc.Link(
                    '回首页',
                    href='/'
                )
            ]
        )

    @staticmethod
    def avoid_debugger(id_):
        import feffery_utils_components.alias as fuc
        from dash import html
        import json
        return fuc.DebugGuardian(
            strategy='debugger-then-execute-js',
            jsString=f'''
                window.dash_clientside.set_props(
                        '{id_}',
                        {{
                            children: JSON.parse('{json.dumps(html.Div([
                html.H1('添加开发者微信').to_plotly_json(),
                fuc.QRCode(value='https://u.wechat.com/MO-Ox1Rul8ehpnQNJQJWlc0', size=256).to_plotly_json()
            ]).to_plotly_json())}')
                        }}
                    )'''
        )
