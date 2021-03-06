# encoding:utf-8
import json
from abc import ABC

import tornado.web
import tool.decorator as decorator
from application.article.helper import articleHelper
from application.user.handler.userHandler import BaseHandler


# something should be shown while step into the home page
# but now I didn't decide what things to show there
# @decorator.exception
# def get(self):
#     self.render('index.html')

class AddArticleHandler(BaseHandler, ABC):
    @decorator.post_exception
    # @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        json_data['ID'] = str(self.get_secure_cookie("ID"), encoding='utf-8')
        ret = articleHelper.add(json_data)
        if ret:
            self.ret['data']['result'] = ret
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Add Article Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Article Has been Exists'


class DeleteArticleHandler(BaseHandler, ABC):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        result = articleHelper.delete(json_data)
        if result is False:
            self.ret['succ'] = False
            self.ret['err'] = 'Article Not Exits'
        else:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Delete Article Successful'


class ModifyArticleHandler(BaseHandler, ABC):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        json_data['ID'] = str(self.get_secure_cookie('ID'), encoding='utf-8')
        ret = articleHelper.modify(json_data)
        if ret:
            self.ret['data']['result'] = ret
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Update Article Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Article Not Exist'


class QueryArticleListHandler(BaseHandler, ABC):
    @decorator.get_exception
    def get(self):
        json_data = json.loads(self.get_argument('param'))
        ret = articleHelper.query_list(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'No Article Find'


class QueryArticleInfoHandler(BaseHandler, ABC):
    @decorator.get_exception
    def get(self):
        json_data = json.loads(self.get_argument('param'))
        ret = articleHelper.query_info(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Article Not Exist'

