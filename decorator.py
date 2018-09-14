from flask import session, redirect, url_for
from functools import wraps




#创建一个登录限制的装饰器
#用户访问某个界面时,如果已经登录则返回该界面,没有登录则跳转到登录界面
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if session.get('user_id'):
            return func(*args, **kw)
        else:
            return redirect(url_for('login'))
    return wrapper