import os

import dash
from flask_login import LoginManager
from configure.security import SECRET_KEY
from flask_login import UserMixin, current_user
from flask import request
from configure.show import WEB_TITLE
from dash_modules.components import main_components
import diskcache
from configure import BASE_PATH
from os.path import join
from huey import SqliteHuey

if not os.path.exists(huey_db_path := join(BASE_PATH, 'task', 'huey_cache')):
    os.makedirs(huey_db_path)
huey = SqliteHuey(filename=join(BASE_PATH, 'task', 'huey_cache', 'cache.db'))
cache = diskcache.Cache(join(BASE_PATH, 'task', 'dash_cache'))
background_callback_manager = dash.DiskcacheManager(cache)

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    update_title=None,
    compress=True,
    background_callback_manager=background_callback_manager,
)
app.server.config['COMPRESS_ALGORITHM'] = 'br'
app.server.config['COMPRESS_BR_LEVEL'] = 9
app.server.secret_key = SECRET_KEY
app.title = WEB_TITLE

server = app.server

#################### 鉴权配置###########################

login_manager = LoginManager()

# 绑定纳入鉴权范围的flask实例
login_manager.init_app(server)


# 给dash定义的鉴权校验的回调
def auth_callback(*args_1, **kwargs_1):
    args_1 = list(args_1)

    def wrapper(func):
        def inner(*args_2, **kwargs_2):
            if not current_user.is_authenticated:
                if len(args_1) > 0:
                    if isinstance(args_1[0], list):
                        return True, *([dash.no_update] * len(args_1[0]))
                    else:
                        return True, dash.no_update
                else:
                    return {i: (dash.no_update if i != 'main-trigger-reload' else True) for i, j in kwargs_1['output'].items()}
            result = func(*args_2, **kwargs_2)
            if len(args_1) > 0:
                if isinstance(args_1[0], list):
                    return False, *result
                else:
                    return False, result
            else:
                result['main-trigger-reload'] = False
                return result

        o = main_components.output_main_trigger_reload
        if len(args_1) > 0:
            if isinstance(args_1[0], list):
                args_1[0].insert(0, o)
            else:
                args_1.insert(0, o)
            app.callback(*args_1, **kwargs_1)(inner)
        else:
            kwargs_1['output']['main-trigger-reload'] = o
        return inner

    return wrapper


app.auth_callback = auth_callback


class User(UserMixin):
    ...


'''
1、在登录成功后，访问current_user.is_authenticated和login_required时就会触发进行login_manager.user_loader鉴权，
判断是否退出登录，退出时更新数据库登录信息：
在初始化layout（is_authenticated） app.py、
dash鉴权回调（is_authenticated） server.py、
20s周期鉴权（is_authenticated） main_c.py、
主页路由鉴权（is_authenticated） main_c.py
2、执行logout，退出登录，退出时更新数据库登录信息
页面idle main_c.py
主动logout
5分钟周期检测activate时间超时 huey_main.py


以保证被挤掉后、过期、用户删除、权限变化后，能及时退出
'''


@login_manager.user_loader
def load_user(user_id):
    curr_user = User()
    curr_user.id = user_id
    dict_userid = eval(user_id)
    name = dict_userid['name']
    session_id = dict_userid['session_id']
    is_admin = dict_userid['is_admin']
    from dao.login import users, users_login_online
    user_attr = users.get_attr(name)
    if (
            # 不在线,并更新active时间
            not users_login_online.is_online(name, session_id, request.remote_addr) or
            # 过期或者用户被删
            not user_attr['is_exists'] or
            user_attr['is_expire'] or
            # 权限变化
            user_attr['is_admin'] != is_admin
    ):
        try:
            users_login_online.pop_online(name, session_id)
        except:
            pass
        finally:
            return None
    return curr_user
