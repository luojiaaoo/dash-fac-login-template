#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : menu.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-21 14:40 
'''
from configure.apps import MENU_ITEMS
import copy


def get_mapping_router_module(accessible_apps, menu_items=None, temp_mapping_router_module=None, prefix=None):
    if menu_items is None:
        menu_items = MENU_ITEMS
    if prefix is None:
        prefix = ['主页', ]
    if temp_mapping_router_module is None:
        mapping_router_module = {}
    else:
        mapping_router_module = temp_mapping_router_module
    for menu_item in menu_items:
        component = menu_item['component']
        if component == 'Item':
            copy_prefix = copy.deepcopy(prefix)
            copy_prefix.append(menu_item['props']['title'])
            if menu_item['props']['key'] in accessible_apps:
                mapping_router_module[menu_item['props']['href']] = (
                    menu_item['props']['key'], menu_item['props']['module_name'], copy_prefix)
        else:
            copy_prefix = copy.deepcopy(prefix)
            copy_prefix.append(menu_item['props']['title'])
            get_mapping_router_module(accessible_apps, menu_item['children'], mapping_router_module, copy_prefix)
    return mapping_router_module


def get_side_menu(accessible_apps):
    _MENU_ITEMS = copy.deepcopy(MENU_ITEMS)

    def get_accessible_app(menu_items_):
        for i, menu_item_ in list(enumerate(menu_items_))[::-1]:
            component = menu_item_['component']
            if component == 'Item':
                if menu_item_['props']['key'] not in accessible_apps:
                    del menu_items_[i]
            else:
                get_accessible_app(menu_item_['children'])

    def remove_empty_submenu(menu_items_):
        for i, menu_item_ in list(enumerate(menu_items_))[::-1]:
            if menu_item_['component'] == 'SubMenu':
                if not menu_item_['children']:
                    del menu_items_[i]
                else:
                    remove_empty_submenu(menu_item_['children'])

    get_accessible_app(_MENU_ITEMS)
    remove_empty_submenu(_MENU_ITEMS)

    return _MENU_ITEMS


def get_all_items():
    menu_items = MENU_ITEMS
    all_items = []

    def get_items(menu_items_):
        for menu_item_ in menu_items_:
            if menu_item_['component'] == 'Item':
                all_items.append(menu_item_['props']['key'])
            else:
                get_items(menu_item_['children'])

    get_items(menu_items)
    return all_items


def get_menu_items(name):
    from dao.login.users import get_permission
    return get_side_menu(get_permission(name))


def get_all_permission():
    return get_all_items()
