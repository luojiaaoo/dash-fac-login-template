#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project : dash-loginV2 
@File    : main_c.py
@IDE     : PyCharm 
@Author  : LUOJA
@Date    : 2024-3-16 17:12 
'''
import datetime
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from server import app
from flask_login import current_user, logout_user
import dash
from dash_modules.components import main_components, msg_components
from loguru import logger
from common import login_user
import dash_modules


# 每20s检测一次，并更新active时间
@app.callback(
    main_components.output_main_trigger_reload,
    main_components.input_main_interval_20s,
    prevent_initial_call=True
)
def check_login(n_intervals):
    if not current_user.is_authenticated:
        return True
    else:
        return False


@app.callback(
    main_components.output_main_trigger_reload,
    [Input('main-idle', 'isIdle'),
     Input('main-header-dropdown', 'nClicks')],
    State('main-header-dropdown', 'clickedKey'),
    prevent_initial_call=True
)
def auto_logout(isIdle, nClicks, clickedKey):
    if isIdle or (nClicks is not None and clickedKey == '退出登录'):
        try:
            from dao.login import users_login_online
            name = login_user.name
            session_id = login_user.session_id
            users_login_online.pop_online(name, session_id)
            logger.info(f'用户{name}登出')
        except:
            pass
        finally:
            if current_user.get_id() is not None:
                logout_user()
                return True
            else:
                return False


@app.callback(
    Output('main-person-info-modal-container', 'children'),
    Input('main-header-dropdown', 'nClicks'),
    State('main-header-dropdown', 'clickedKey'),
    prevent_initial_call=True
)
def add_person_info_modal(nClicks, clickedKey):
    if nClicks is not None:
        name = login_user.name
        from dao.login.users import get_info
        dict_user_info = get_info(name)
        if clickedKey == '个人资料':
            return fac.AntdModal(
                [
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(
                                fac.AntdText(
                                    name,
                                    copyable=True
                                ),
                                label='用户名'
                            ),
                            fac.AntdFormItem(
                                fac.AntdText(
                                    '是' if dict_user_info['is_admin'] else '否',
                                ),
                                label='是否管理员'
                            ),
                            fac.AntdFormItem(
                                fac.AntdText(
                                    dict_user_info['create_time']
                                    .strftime(
                                        '%Y-%m-%d %H:%M:%S'
                                    ),
                                ),
                                label='注册时间'
                            ),
                            fac.AntdFormItem(
                                fac.AntdText(
                                    f"{dict_user_info['expire_time']:%Y-%m-%d %H:%M:%S}"
                                ),
                                label='失效时间'
                            )
                        ],
                        labelCol={
                            'span': 4
                        }
                    )
                ],
                title='个人资料',
                mask=False,
                visible=True
            )
        if clickedKey == '修改密码':
            return fac.AntdModal(
                [
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id='main-change-new-password',
                                    passwordUseMd5=True,
                                    mode='password',
                                ),
                                label='新密码',
                            ),
                            fuc.FefferyFancyButton(
                                '确认修改',
                                type='secondary',
                                ripple=True,
                                debounceWait=500,
                                id='main-change-password-btn'
                            )
                        ],
                        labelCol={
                            'span': 4
                        }
                    )
                ],
                title='修改密码',
                mask=False,
                visible=True
            )
        if clickedKey == '用户管理':
            from dao.login.users import get_data_summary_for_user_manager
            data, summary = get_data_summary_for_user_manager()
            return fac.AntdModal(
                [
                    fac.AntdSpace(
                        [fac.AntdInput(
                            id='main-table-user-manager-add-name',
                            prefix=fac.AntdIcon(
                                icon='antd-user'
                            ),
                            placeholder='请输入用户名',
                            style={
                                'width': 200
                            }
                        ),
                            fac.AntdButton('添加', id='main-table-user-manager-add', style={'margin-right': '50px'}),
                            fac.AntdPopconfirm(
                                fac.AntdButton('删除', danger=True),
                                title=f'确认删除吗',
                                placement='topLeft',
                                id='main-table-user-manager-delete',
                            ),
                        ], style={'margin-bottom': '10px'}
                    ),
                    fac.AntdTable(
                        id='main-table-user-manager',
                        columns=[
                            {
                                'title': '用户',
                                'dataIndex': '用户',
                                'width': 'calc(100% / 10)'
                            },
                            {
                                'title': '密码',
                                'dataIndex': '密码',
                                'renderOptions': {
                                    'renderType': 'button',
                                    'renderButtonPopConfirmProps': {
                                        'title': '确认重置？',
                                        'okText': '确认',
                                        'cancelText': '取消'
                                    }
                                }
                            },
                            {
                                'title': '管理员',
                                'dataIndex': '管理员',
                                'renderOptions': {
                                    'renderType': 'switch'
                                }
                            },
                            {
                                'title': '失效时间',
                                'dataIndex': '失效时间',
                                'editable': True,
                                'width': 'calc(100%*2 / 10)'
                            },
                            {
                                'title': '设置有效天数',
                                'dataIndex': '设置有效天数',
                                'renderOptions': {
                                    'renderType': 'button',
                                    'renderButtonPopConfirmProps': {
                                        'title': '确认执行？',
                                        'okText': '确认',
                                        'cancelText': '取消'
                                    }
                                }
                            },
                            {
                                'title': '应用权限',
                                'dataIndex': '应用权限',
                                'renderOptions': {
                                    'renderType': 'select'
                                },
                                'width': 'calc(100%*6 / 10)'
                            },
                        ],
                        data=data,
                        columnsFormatConstraint={
                            '失效时间': {
                                'rule': r'(((^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(10|12|0?[13578])([-\/\._])(3[01]|[12][0-9]|0?[1-9]))|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(11|0?[469])([-\/\._])(30|[12][0-9]|0?[1-9]))|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(0?2)([-\/\._])(2[0-8]|1[0-9]|0?[1-9]))|(^([2468][048]00)([-\/\._])(0?2)([-\/\._])(29))|(^([3579][26]00)([-\/\._])(0?2)([-\/\._])(29))|(^([1][89][0][48])([-\/\._])(0?2)([-\/\._])(29))|(^([2-9][0-9][0][48])([-\/\._])(0?2)([-\/\._])(29))|(^([1][89][2468][048])([-\/\._])(0?2)([-\/\._])(29))|(^([2-9][0-9][2468][048])([-\/\._])(0?2)([-\/\._])(29))|(^([1][89][13579][26])([-\/\._])(0?2)([-\/\._])(29))|(^([2-9][0-9][13579][26])([-\/\._])(0?2)([-\/\._])(29)))((\s+(0?[1-9]|1[012])(:[0-5]\d){0,2}(\s[AP]M))?$|(\s+([01]\d|2[0-3])(:[0-5]\d){0,2})?$))',
                                'content': '请输入正确时间格式'
                            },
                        },
                        pagination={
                            'pageSize': 5,
                            'showSizeChanger': True,
                            'pageSizeOptions': [5, 10, 20]
                        },
                        sortOptions={
                            'sortDataIndexes': ['用户', '失效时间', ]
                        },
                        filterOptions={
                            '用户': {
                                'filterSearch': True
                            }
                        },
                        bordered=True,
                        rowSelectionType='radio',
                        summaryRowContents=summary
                    )
                ],
                title='用户管理',
                visible=True,
                width='1300px',
            )
    return dash.no_update


@app.auth_callback(
    main_components.output_main_message_popup,
    Input('main-change-password-btn', 'nClicks'),
    [State('main-change-new-password', 'md5Value'),
     State('main-change-new-password', 'value')],
    prevent_initial_call=True,
)
def change_password(nClicks, md5Value, value):
    if nClicks and value:
        name = login_user.name
        try:
            from dao.login.users import change_password
            change_password(name, md5Value)
        except:
            logger.warning(f'{name}-密码修改失败')
            return msg_components.message(f'{name}-密码修改失败', 'error')
        else:
            logger.info(f'{name}-密码修改为{value}')
            return msg_components.message(f'{name}-密码修改成功', 'success')
    return dash.no_update


@app.auth_callback(
    [Output('main-table-user-manager', 'data', allow_duplicate=True),
     Output('main-table-user-manager', 'summaryRowContents', allow_duplicate=True),
     main_components.output_main_message_popup],
    [
        # 失效时间
        Input('main-table-user-manager', 'recentlyChangedRow'),
        Input('main-table-user-manager', 'recentlyChangedColumn'),
        # 管理员
        Input('main-table-user-manager', 'recentlySwitchDataIndex'),
        Input('main-table-user-manager', 'recentlySwitchStatus'),
        Input('main-table-user-manager', 'recentlySwitchRow'),
        # 重置密码
        Input('main-table-user-manager', 'nClicksButton'),
        # 权限
        Input('main-table-user-manager', 'recentlySelectRow'),
        Input('main-table-user-manager', 'recentlySelectDataIndex'),
        Input('main-table-user-manager', 'recentlySelectValue'),
    ],
    State('main-table-user-manager', 'clickedCustom'),
    prevent_initial_call=True,
)
def user_manager(ChangedRow, ChangedColumnm, SwitchDataIndex, SwitchStatus, SwitchRow, nClicksButton, recentlySelectRow, SelectDataIndex, SelectValue,
                 clickedCustom):
    if not any([ChangedRow, ChangedColumnm, SwitchDataIndex, SwitchStatus, SwitchRow, nClicksButton, recentlySelectRow, SelectDataIndex, SelectValue,
                clickedCustom]):
        return dash.no_update, dash.no_update, dash.no_update
    # print(dash.ctx.triggered)
    # print('\n'.join([str(i) for i in
    #                  [ChangedRow, ChangedColumnm, SwitchDataIndex, SwitchStatus, SwitchRow, nClicksButton, recentlySelectRow, SelectDataIndex,
    #                   SelectValue, clickedCustom]]))
    from dao.login.users import get_data_summary_for_user_manager
    # 重置密码
    if dash.ctx.triggered[0]['prop_id'] == 'main-table-user-manager.nClicksButton':
        if clickedCustom.split()[0] == 'reset-password':
            name = clickedCustom.split()[-1]
            from dao.login.users import reset_password
            try:
                passwd = reset_password(name)
            except:
                logger.warning(f'{name}-密码重置失败')
                return dash.no_update, dash.no_update, msg_components.message(f'{name}-密码重置失败', 'error')
            else:
                logger.info(f'{name}-密码重置为{passwd}')
                return *get_data_summary_for_user_manager(), msg_components.message(f'{name}-密码重置为{passwd}', 'success', 6)
        elif clickedCustom.split()[0] == 'set-expire-time':
            name = clickedCustom.split()[-1]
            days = clickedCustom.split()[-2]
            if days == '过期':
                days = -1
            from dao.login.users import modify_valid_time
            try:
                modify_valid_time(name, datetime.timedelta(days=int(days)))
            except:
                logger.warning(f'{name}-有效期设置{days}天失败')
                return dash.no_update, dash.no_update, msg_components.message(f'{name}-有效期设置失败', 'error')
            else:
                logger.info(f'{name}-有效期{days}天，设置成功')
                return *get_data_summary_for_user_manager(), msg_components.message(f'{name}-有效期{days}天，设置成功', 'success')
    elif dash.ctx.triggered[0]['prop_id'] == 'main-table-user-manager.recentlySwitchRow' and SwitchDataIndex == '管理员':
        from dao.login.users import modify_admin
        name = SwitchRow['用户']
        try:
            modify_admin(name, SwitchStatus)
        except:
            logger.warning(f'{name}-管理员设置为{SwitchStatus}失败')
            return dash.no_update, dash.no_update, msg_components.message(f'{name}-管理员权限失败', 'error')
        else:
            logger.info(f'{name}-管理员设置为{SwitchStatus}成功')
            return *get_data_summary_for_user_manager(), msg_components.message(f'{name}-管理员权限' + ('设置成功' if SwitchStatus else '取消成功'), 'success')
    elif dash.ctx.triggered[0]['prop_id'] == 'main-table-user-manager.recentlyChangedRow' and ChangedColumnm == '失效时间':
        name = ChangedRow['用户']
        expire_time = datetime.datetime.strptime(ChangedRow['失效时间'], '%Y-%m-%d %H:%M:%S')
        from dao.login.users import modify_expire_time
        try:
            modify_expire_time(name, expire_time)
        except:
            logger.warning(f'{name}-失效时间{ChangedRow["失效时间"]}设置失败')
            return dash.no_update, dash.no_update, msg_components.message(f'{name}-失效时间设置失败', 'error')
        else:
            logger.info(f'{name}-失效时间{ChangedRow["失效时间"]}设置成功')
            return *get_data_summary_for_user_manager(), msg_components.message(f'{name}-失效时间设置成功', 'success')
    elif dash.ctx.triggered[0]['prop_id'] == 'main-table-user-manager.recentlySelectRow' and SelectDataIndex == '应用权限':
        name = recentlySelectRow['用户']
        permission = SelectValue
        from dao.login.users import modify_permission
        try:
            modify_permission(name, permission)
        except:
            logger.warning(f'{name}-应用权限设置失败')
            return dash.no_update, dash.no_update, msg_components.message(f'{name}-应用权限设置失败', 'error')
        else:
            logger.info(f'{name}-应用权限设置成功-{",".join(permission)}')
            return *get_data_summary_for_user_manager(), msg_components.message(f'{name}-应用权限设置成功', 'success')
    return dash.no_update, dash.no_update, dash.no_update


@app.auth_callback(
    [main_components.output_main_message_popup,
     Output('main-table-user-manager', 'data', allow_duplicate=True),
     Output('main-table-user-manager', 'summaryRowContents', allow_duplicate=True)],
    [Input('main-table-user-manager-delete', 'confirmCounts'),
     Input('main-table-user-manager-add', 'nClicks')],
    [State('main-table-user-manager', 'selectedRowKeys'),
     State('main-table-user-manager-add-name', 'value')],
    prevent_initial_call=True,
)
def add_delete_user(confirmCounts, nClicks, selectedRowKeys, value):
    if nClicks is None and confirmCounts is None:
        return dash.no_update, dash.no_update, dash.no_update
    from dao.login.users import get_data_summary_for_user_manager
    if dash.ctx.triggered[0]['prop_id'] == 'main-table-user-manager-delete.confirmCounts':
        from dao.login.users import delete_user
        name = selectedRowKeys[0]
        try:
            delete_user(name)
        except:
            logger.warning(f'删除用户{name}失败')
            msg = msg_components.message(f'删除用户{name}失败', 'error')
        else:
            logger.info(f'删除用户{name}成功')
            msg = msg_components.message(f'删除用户{name}成功', 'success')
        data, summary = get_data_summary_for_user_manager()
        return msg, data, summary
    if dash.ctx.triggered[0]['prop_id'] == 'main-table-user-manager-add.nClicks':
        from dao.login.users import creatr_user
        name = value
        try:
            passwd = creatr_user(name)
        except:
            logger.warning(f'添加用户{name}失败')
            msg = msg_components.message(f'添加用户{name}失败', 'error')
        else:
            logger.info(f'添加用户{name}成功，密码为{passwd}')
            msg = msg_components.message(f'添加用户{name}成功，密码为{passwd}', 'success', 6)
        data, summary = get_data_summary_for_user_manager()
        return msg, data, summary


@app.auth_callback(
    [Output('main-container', 'children'),
     Output('side-menu', 'currentKey'),
     Output('main-item-breadcrumb', 'items')],
    Input('main-url', 'pathname'),
    prevent_initial_call=True,
)
def render_main_container(pathname):
    from dao.login.users import get_permission
    name = login_user.name
    from common.dash_assist.menu import get_mapping_router_module, get_all_items
    mapping_router_module_all = get_mapping_router_module(get_all_items())
    mapping_router_module_person = get_mapping_router_module(get_permission(name))
    if pathname in list(mapping_router_module_all.keys()):
        if pathname not in list(mapping_router_module_person.keys()):
            return [main_components.go_login('没有访问该应用的权限'),
                    mapping_router_module_all[pathname][0],
                    [{'title': i} for i in mapping_router_module_all[pathname][2]]]
        for pn, (menu_key, module_name, breadcrumb) in mapping_router_module_person.items():
            if pathname == pn:
                return [
                    eval('dash_modules.views.' + module_name + '.render()'),
                    menu_key,
                    [{'title': i} for i in breadcrumb]
                ]
    return main_components.go_login('当前页面不存在'), None, [{'title': '当前页面不存在'}, ]
