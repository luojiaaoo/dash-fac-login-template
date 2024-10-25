#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : apps.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-19 19:09 
'''

MENU_ITEMS = [
    {
        'component': 'Item',
        'props': {
            'title': '数据总览',
            'key': '数据总览',
            'module_name': 'index',
            'icon': 'antd-dashboard',
            'href': '/',
        }
    },
    {
        'component': 'SubMenu',
        'props': {
            'title': 'app1',
            'icon': 'antd-car'
        },
        'children': [
            {
                'component': 'Item',
                'props': {
                    'title': 'Application1',
                    # 用于权限控制
                    'key': 'app1.Application1',
                    # 用于自动模块导入
                    'module_name': 'app1.aa',
                    'icon': 'antd-dashboard',
                    'href': '/app1/aa',
                }
            },
            {
                'component': 'Item',
                'props': {
                    'title': 'Application2',
                    'key': 'app1.Application2',
                    'module_name': 'app1.bb',
                    'icon': 'antd-dashboard',
                    'href': '/app1/bb',
                }
            },
        ]
    },
]

if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(Path(__file__).parent.parent.__str__())
    from common.dash_assist.menu import get_all_items, get_side_menu, get_mapping_router_module

    print(get_side_menu(['测试应用3', '测试应用2']))
    print(get_mapping_router_module(['数据总览', '测试应用3', '测试应用2']))
    print(get_all_items())
