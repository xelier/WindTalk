# encoding:utf-8
import json
from abc import ABC

import tornado.web
import tool.decorator as decorator
from application.user.helper import userhelper


# something should be shown while step into the home page
# but now I didn't decide what things to show there
# @decorator.exception
# def get(self):
#     self.render('index.html')

class BaseHandler(tornado.web.RequestHandler, ABC):
    def get_current_user(self):
        return self.get_secure_cookie("ID")


class WelcomeHandler(tornado.web.RequestHandler, ABC):
    def get(self):
        self.render('index.html', user=self.current_user)


class RegisterHandler(tornado.web.RequestHandler, ABC):
    @decorator.post_exception
    def post(self):
        json_data = json.loads(self.request.body)
        ret = userhelper.register(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Register Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Has benn Exists'


class LoginHandler(tornado.web.RequestHandler, ABC):
    @decorator.post_exception
    # @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        username = json_data['USERNAME']
        password = json_data['PASSWORD']
        role = json_data['ROLE']
        result = userhelper.login(username, password, role)
        if result is False:
            self.ret['succ'] = False
            self.ret['err'] = 'User not exits or Password is wrong'
        else:
            self.ret['data']['USERNAME'] = result['USERNAME']
            self.set_secure_cookie("USERNAME", result['USERNAME'])
            self.set_secure_cookie("ID", str(result['ID']))


class ModifyUser(tornado.web.RequestHandler, ABC):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        json_data = json.load(self.request.body)
        ret = userhelper.modify(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Update Profile Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist'


class ModifyPwd(tornado.web.RequestHandler, ABC):
    @tornado.web.authenticated
    @decorator.post_exception
    def post(self):
        json_data = json.load(self.request.body)
        ret = userhelper.modify_pwd(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Update Password Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist Or Origin Password Is Wrong'


class GetUserInfo(tornado.web.RequestHandler, ABC):
    @decorator.get_exception
    @tornado.web.authenticated
    def get(self):
        json_data = json.load(self.get_argument('param'))
        ret = userhelper.query_user_info(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist'


class UserExit(tornado.web.RequestHandler, ABC):
    def post(self):
        self.clear_cookie("ID")
        self.clear_cookie("USERNAME")
        self.redirect("/")
