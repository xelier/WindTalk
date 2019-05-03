# encoding:utf-8
import json
from abc import ABC

import tornado.web
import tool.decorator as decorator
from application.user.helper import userHelper


# something should be shown while step into the home page
# but now I didn't decide what things to show there
# @decorator.exception
# def get(self):
#     self.render('index.html')

class BaseHandler(tornado.web.RequestHandler, ABC):
    def get_current_user(self):
        return self.get_secure_cookie("ID")

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class WelcomeHandler(BaseHandler, ABC):
    def get(self):
        self.render('index.html', user=self.current_user)


class RegisterHandler(BaseHandler, ABC):
    @decorator.post_exception
    def post(self):
        json_data = json.loads(self.request.body)
        ret = userHelper.register(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Register Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Has been Exists'


class LoginHandler(BaseHandler, ABC):
    @decorator.post_exception
    # @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        username = json_data['USERNAME']
        password = json_data['PASSWORD']
        role = json_data['ROLE']
        result = userHelper.login(username, password, role)
        if result is False:
            self.ret['succ'] = False
            self.ret['err'] = 'User not exits or Password is wrong'
        else:
            self.ret['succ'] = True
            self.ret['data']['USERNAME'] = result['USERNAME']
            self.set_secure_cookie("USERNAME", result['USERNAME'])
            self.set_secure_cookie("ID", str(result['ID']))


class ModifyUserHandler(BaseHandler, ABC):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        json_data = json.load(self.request.body)
        json_data['ID'] = self.get_secure_cookie('ID')
        ret = userHelper.modify(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Update Profile Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist'


class ModifyPwdHandler(BaseHandler, ABC):
    @tornado.web.authenticated
    @decorator.post_exception
    def post(self):
        json_data = json.load(self.request.body)
        json_data['ID'] = self.get_secure_cookie('ID')
        ret = userHelper.modify_pwd(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Update Password Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist Or Origin Password Is Wrong'


class GetUserInfoHandler(BaseHandler, ABC):
    @decorator.get_exception
    @tornado.web.authenticated
    def get(self):
        json_data = json.load(self.get_argument('param'))
        ret = userHelper.query_user_info(json_data)
        ret['ID'] = self.get_secure_cookie('ID')
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist'


class UserExitHandler(BaseHandler, ABC):
    def post(self):
        self.clear_cookie("ID")
        self.clear_cookie("USERNAME")
        self.redirect("/")
