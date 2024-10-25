#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : main.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-15 16:14 
'''
from dash import html, dcc, get_asset_url
import feffery_antd_components.alias as fac
import feffery_utils_components.alias as fuc
from configure.show import LOGO_PATH
from configure.show import SYSTEM_NAME, SYSTEM_NAME_SUB, CONTACT_WAY
from common.dash_assist.menu import get_menu_items
from dash_modules.components import main_components
from common import login_user
import dash_modules.callbacks.enter.main_c


def render_content():
    is_admin = login_user.is_admin
    name = login_user.name
    return html.Div(
        id='main-full-container',
        children=[
            # 防止debugger
            *([main_components.avoid_debugger('main-full-container')] if not is_admin else []),
            # 自动检测登录情况
            fuc.Reload(id='main-trigger-reload'),
            dcc.Interval(id='main-interval-20s', interval=1000 * 20),
            fuc.Idle(id='main-idle', waitDuration=1000 * 60 * 30),
            # url监听
            fuc.Location(id='main-url'),
            # 个人信息modal容器
            html.Div(id='main-person-info-modal-container'),
            # 文件文本下载
            dcc.Download(id="main-download-text"),
            # 全局信息提示
            html.Div(id='main-message-popup'),
            fac.ConfigProvider(
                fac.Row(
                    [
                        # 侧边菜单
                        fac.Col(
                            fac.Affix(
                                html.Div(
                                    [
                                        fac.Space(
                                            [
                                                fac.Space(
                                                    [
                                                        fac.Image(
                                                            src=get_asset_url(LOGO_PATH),
                                                            height=50,
                                                            preview=False
                                                        ),
                                                        fac.Space(
                                                            [
                                                                fac.Text(
                                                                    SYSTEM_NAME,
                                                                    italic=True,
                                                                    strong=True,
                                                                    style={
                                                                        'fontSize': 25,
                                                                        'letter-spacing': '-3px'
                                                                    }
                                                                ),
                                                                fac.Text(
                                                                    SYSTEM_NAME_SUB,
                                                                    strong=True,
                                                                    style={
                                                                        'color': '#adb5bd',
                                                                        'fontSize': 15
                                                                    }
                                                                )
                                                            ],
                                                            direction='vertical',
                                                            size=0
                                                        )
                                                    ],
                                                    style={
                                                        'width': '100%',
                                                        'padding': '20px 30px'
                                                    }
                                                ),
                                                fuc.Style(
                                                    rawStyle='''
#side-menu {
    background: transparent !important;
}

#side-menu .ant-menu-item-selected {
    background: #335efb !important;
    color: white !important;
    border-radius: 6px;
}

#side-menu .ant-menu-item-selected * {
    color: white !important;
}

#side-menu .ant-menu-item {
    border-radius: 6px;
}

#side-menu .ant-menu-item-selected::after {
    border-right: none !important;
}
'''
                                                ),
                                                fac.Menu(
                                                    id='side-menu',
                                                    mode='inline',
                                                    menuItems=get_menu_items(name),
                                                    style={
                                                        'padding': '0 20px'
                                                    }
                                                )
                                            ],
                                            direction='vertical',
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        fac.Row(
                                            [
                                                fac.Col(
                                                    fac.Space(
                                                        [
                                                            fac.Icon(
                                                                icon=CONTACT_WAY[0],
                                                                style={
                                                                    'fontSize': '28px'
                                                                }
                                                            ),
                                                            CONTACT_WAY[1]
                                                        ]
                                                    )
                                                ),
                                                fac.Col(
                                                    CONTACT_WAY[2]
                                                )
                                            ],
                                            justify='space-between',
                                            align='middle',
                                            style={
                                                'position': 'absolute',
                                                'bottom': 0,
                                                'background': '#f0effd',
                                                'width': '100%',
                                                'padding': '20px 20px',
                                                'color': '#a6a9b6'
                                            }
                                        )
                                    ],
                                    style={
                                        'width': 250,
                                        'background': '#f8f9fd',
                                        'height': '100vh',
                                        'position': 'relative'
                                    }
                                ),
                                offsetTop=0
                            ),
                            flex='none'
                        ),
                        fac.Col(
                            [
                                # 内容区页首
                                fac.Affix(
                                    fac.Row(
                                        [
                                            # 头
                                            fac.Col(
                                                fac.Breadcrumb(items=[], id='main-item-breadcrumb',
                                                               style={'font-size': 'large'})
                                            ),
                                            fac.Col(
                                                fac.Space(
                                                    [
                                                        # 个人信息
                                                        fac.Space(
                                                            [
                                                                fac.Tooltip(
                                                                    fac.Avatar(
                                                                        mode='text',
                                                                        size=36,
                                                                        text=name,
                                                                        style={
                                                                            'background': 'gold' if is_admin else '#ff6b81'
                                                                        }
                                                                    ),
                                                                    title='当前用户：' + name,
                                                                    placement='bottom'
                                                                ),
                                                                fac.Text(
                                                                    children='管理员' if is_admin else '普通用户',
                                                                    style={
                                                                        'color': '#c0c0c8'
                                                                    }
                                                                ),
                                                                fac.Dropdown(
                                                                    id='main-header-dropdown',
                                                                    title='个人中心',
                                                                    arrow=True,
                                                                    menuItems=[
                                                                        {
                                                                            'title': '个人资料',
                                                                            'key': '个人资料'
                                                                        },
                                                                        {
                                                                            'title': '修改密码',
                                                                            'key': '修改密码'
                                                                        },
                                                                        *(
                                                                            [{
                                                                                'title': '用户管理',
                                                                                'key': '用户管理'
                                                                            }] if is_admin else []
                                                                        ),
                                                                        {
                                                                            'isDivider': True
                                                                        },
                                                                        {
                                                                            'title': '退出登录',
                                                                            'key': '退出登录'
                                                                        },
                                                                    ],
                                                                    placement='bottomRight',
                                                                    overlayStyle={
                                                                        'width': '125px'
                                                                    }
                                                                )
                                                            ],
                                                            size='small',
                                                        )
                                                    ],
                                                    size=40,
                                                    style={
                                                        'paddingRight': 10
                                                    }
                                                )
                                            )
                                        ],
                                        justify='space-between',
                                        style={
                                            'padding': '20px 30px',
                                            'boxShadow': 'rgb(240 241 242) 0px 2px 14px',
                                            'background': 'white'
                                        }
                                    ),
                                    offsetTop=0
                                ),
                                html.Div(
                                    id='main-container',
                                    style={
                                        'padding': 25
                                    }
                                ),
                            ],
                            flex='auto'
                        )
                    ],
                    wrap=False
                ),
                primaryColor='#335efb'
            )
        ]
    )
