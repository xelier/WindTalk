# encoding:utf-8
import json
from abc import ABC

import tornado.web
import tool.decorator as decorator
from core import sqlhelper
from application.user.helper import userhelper


class IndexHandler(tornado.web.RequestHandler, ABC):
    # something should be shown while step into the home page
    # but now I didn't decide what things to show there
    @decorator.exception
    def get(self):
        self.render('index.html')

    @decorator.post_exception
    def post(self):
        user = sqlhelper.get_all_record_list('user', {})
        res = []
        user_info = {}
        for us in user:
            user_info['username'] = us['username']
            user_info['profile'] = us['profile']
            res.append(user_info)
        self.ret['data'] = res


class LoginHandler(tornado.web.RequestHandler, ABC):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        username = json_data['USERNAME']
        password = json_data['PASSWORD']
        role = json_data['ROLE']
        ret = userhelper.login(username, password, role)
        if not ret:
            self.ret['succ'] = False
            self.ret['err'] = 'User not exits or Password is wrong'
        else:
            self.ret['data']['username'] = ret


class UserExit(tornado.web.RequestHandler, ABC):
    pass
