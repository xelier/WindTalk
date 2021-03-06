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
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8080")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')


class WelcomeHandler(BaseHandler, ABC):
    def get(self):
        self.render('index.html', user=self.get_secure_cookie('USER_NAME'))


class RegisterHandler(BaseHandler, ABC):
    @decorator.post_exception
    def post(self):
        json_data = json.loads(self.request.body)
        ret = userHelper.register(json_data)
        if ret is not None:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Register Successful'
            self.ret['data']['result'] = ret
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
        role = '0'
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
        json_data = json.loads(self.request.body)
        if json_data['ID'] is None:
            json_data['ID'] = str(self.get_secure_cookie("ID"), encoding='utf-8')
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
        json_data['ID'] = str(self.get_secure_cookie('ID'), encoding='utf-8')
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
        json_data['ID'] = str(self.get_secure_cookie("ID"), encoding='utf-8')
        ret = userHelper.query_user_info(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'User Not Exist'


class UserExitHandler(BaseHandler, ABC):
    @tornado.web.authenticated
    @decorator.get_exception
    def get(self):
        self.clear_cookie("ID")
        self.clear_cookie("USERNAME")
        self.ret['succ'] = True
        self.ret['data']['resultDesc'] = 'exit success'
        self.redirect("/")


class CurrentUserHandler(BaseHandler, ABC):
    # @tornado.web.authenticated
    @decorator.get_exception
    def get(self):
        ret = {'USERNAME': self.get_secure_cookie('USERNAME')}
        if ret['USERNAME'] is not None:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'user already login'
            self.ret['data']['USERNAME'] = ret['USERNAME']
        else:
            self.ret['succ'] = False
            self.ret['data']['resultDesc'] = 'user not login'


class QueryUserPageHandler(BaseHandler, ABC):
    @decorator.get_exception
    def get(self):
        json_data = json.loads(self.get_argument("param"))
        ret = userHelper.query_user_list(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'No Comment Found'


class DeleteUserHandler(BaseHandler, ABC):
    @tornado.web.authenticated
    @decorator.post_exception
    def post(self):
        json_data = json.loads(self.request.body)
        ret = userHelper.detele_user(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Delete User Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Delete User Failed'
