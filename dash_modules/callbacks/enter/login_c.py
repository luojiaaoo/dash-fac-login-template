import traceback

import dash
from dash.dependencies import Input, Output, State
from server import app, User
from dao.login import users, users_login_online
from flask import request
from flask_login import login_user
import feffery_antd_components.alias as fac
from loguru import logger


@app.callback(
    [Output('login-username-form-item', 'validateStatus'),
     Output('login-password-form-item', 'validateStatus'),
     Output('login-username-form-item', 'help'),
     Output('login-password-form-item', 'help'),
     Output('login-trigger-reload', 'reload')],
    [Input('login-submit', 'nClicks'),
     Input('login-password', 'nSubmit')],
    [State('login-username', 'value'),
     State('login-password', 'md5Value'),
     State('login-password', 'value')],
    prevent_initial_call=True
)
def login_auth(nClicks, nSubmit, name, password_md5, password):
    # 校验全部输入值是否不为空
    if all([name, password]):
        user_attr = users.get_attr(name, password_md5)
        # 校验用户名是否存在
        if not user_attr['is_exists']:
            return [
                'error',
                None,
                '用户不存在！',
                None,
                False
            ]
        if user_attr['is_expire']:
            return [
                'error',
                None,
                '用户已过期！',
                None,
                False
            ]
        if user_attr['is_valid']:
            current_user = User()
            import uuid
            session_id = str(uuid.uuid4())
            is_admin = user_attr['is_admin']
            current_user.id = {"name": name, "session_id": session_id, 'is_admin': is_admin}
            try:
                users_login_online.insert_login_online(
                    name=name,
                    session_id=session_id,
                    ip=request.remote_addr
                )
            except:
                traceback.print_exc()
                return [
                    'error',
                    None,
                    '用户登录错误，请重试！',
                    None,
                    False
                ]
            login_user(current_user)
            logger.info(f'用户{name}登录成功')
            return [
                None,
                None,
                None,
                None,
                True
            ]
        else:
            return [
                None,
                'error',
                None,
                '密码错误！',
                False
            ]
    return [
        None if name else 'error',
        None if password else 'error',
        None if name else '请输入用户名！',
        None if password else '请输入密码！',
        False
    ]


# 管理员后门
@app.callback(
    Output('login-register-modal', 'visible'),
    Input('login-register', 'nClicks'),
    State('login-url', 'hash'),
    prevent_initial_call=True
)
def show_register_modal(nClicks, url_hash):
    from configure.security import TRICK_HASH_LOGIN
    if url_hash == TRICK_HASH_LOGIN:
        return True
    else:
        return dash.no_update


@app.callback(
    Output('login-register-note', 'children'),
    Input('login-register-modal', 'okCounts'),
    [State('login-register-name', 'value'),
     State('login-register-password', 'md5Value'),
     State('login-register-password', 'value'),
     State('login-url', 'hash')],
    prevent_initial_call=True
)
def register(okCounts, name, md5_password, password, url_hash):
    from configure.security import TRICK_HASH_LOGIN
    if url_hash == TRICK_HASH_LOGIN:
        if all([name, password]):
            from dao.login.users import register
            is_success = register(name, md5_password, is_admin=True)
            if is_success:
                return fac.Message(
                    content=f'{name}-注册成功',
                    type='success'
                )
            else:
                return fac.Message(
                    content=f'{name}-用户已存在',
                    type='error'
                )
        else:
            return fac.Message(
                content=f'请填写用户名和密码',
                type='error'
            )
    else:
        return dash.no_update
