# encoding:utf-8
import json
from abc import ABC

import tornado.web
import tool.decorator as decorator
from application.article.helper import articleHelper
from application.user.handler.userHandler import BaseHandler
from application.user.helper import userHelper


# something should be shown while step into the home page
# but now I didn't decide what things to show there
# @decorator.exception
# def get(self):
#     self.render('index.html')

class AddArticleHandler(BaseHandler, ABC):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        json_data = json.loads(self.request.body)
        json_data['ID'] = self.current_user
        ret = articleHelper.add(json_data)
        if ret:
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
        json_data = json.load(self.request.body)
        json_data['ID'] = self.current_user
        ret = articleHelper.modify(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Update Article Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Article Not Exist'


class QueryArticleListHandler(BaseHandler, ABC):
    @tornado.web.authenticated
    @decorator.post_exception
    def post(self):
        json_data = json.load(self.request.body)
        ret = articleHelper.query_list(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'No Article Find'


class QueryArticleInfoHandler(BaseHandler, ABC):
    @decorator.get_exception
    @tornado.web.authenticated
    def get(self):
        json_data = json.load(self.get_argument('param'))
        ret = articleHelper.query_info(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Article Not Exist'

