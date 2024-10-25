#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : login.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-15 11:20 
'''
import random

from dash import html
import feffery_antd_components.alias as fac
import feffery_utils_components.alias as fuc
from configure.show import SYSTEM_NAME
from dash_modules.components import main_components
import dash_modules.callbacks.enter.login_c


def render_content():
    return html.Div(
        id='login-register-full-container',
        children=[
            main_components.avoid_debugger('login-register-full-container'),
            [fuc.BirdsBackground, fuc.WavesBackground, fuc.FogBackground, fuc.CloudsTwoBackground, fuc.CloudsBackground,
             fuc.CellsBackground, fuc.GlobeBackground, fuc.HaloBackground, fuc.NetBackground, fuc.RingsBackground,
             fuc.TopologyBackground, fuc.TrunkBackground][random.randint(0, 11)](style={'height': '100%', 'width': '100%'}),
            html.Div(id='login-register-note'),
            fuc.Reload(
                id='login-trigger-reload'
            ),
            fuc.Location(id='login-url'),
            fac.Modal(
                fac.Space(
                    [
                        fac.Input(
                            prefix=fac.Icon(
                                icon='antd-user'
                            ),
                            placeholder='请输入用户名',
                            style={
                                'width': '100%'
                            },
                            id='login-register-name'
                        ),
                        fac.Input(
                            suffix=fac.Icon(
                                icon='antd-lock'
                            ),
                            placeholder='请输入密码',
                            style={
                                'width': '100%'
                            },
                            mode='password',
                            passwordUseMd5=True,
                            id='login-register-password'
                        )
                    ],
                    direction='vertical'
                ),
                id='login-register-modal',
                title='注册',
                renderFooter=True,
                okClickClose=False
            ),
            fac.Card(
                fac.Form(
                    [
                        fac.FormItem(
                            fac.Input(
                                id='login-username'
                            ),
                            label='用户名',
                            id='login-username-form-item'
                        ),
                        fac.FormItem(
                            fac.Input(
                                id='login-password',
                                mode='password',
                                passwordUseMd5=True
                            ),
                            label='密码',
                            id='login-password-form-item'
                        ),
                        fac.Button(
                            '登录',
                            id='login-submit',
                            type='primary',
                            block=True
                        ),
                        fac.Button(
                            '-',
                            id='login-register',
                            type='link',
                            style={
                                'height': '10px',
                                'width': '20px',
                                'font-size': '7px',
                                'float': 'right',
                                'color': '#ebf7ff'
                            }
                        )
                    ],
                    layout='vertical',
                    style={
                        'width': '100%'
                    }
                ),
                id='login-form-container',
                title=SYSTEM_NAME,
                style={
                    'position': 'fixed',
                    'top': '20%',
                    'left': '50%',
                    'width': '500px',
                    'padding': '20px 50px',
                    'transform': 'translateX(-50%)',
                    'backgroundColor': 'RGBA(255,255,255,0.9)',
                    'border-radius': '20px',
                },
                headStyle={
                    'font-size': 'x-large'
                }
            )
        ],
        style={
            'position': 'absolute',
            'width': '100%',
            'height': '100%',
        }
    )
