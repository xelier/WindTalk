#encoding:utf-8
import json

import tornado
import tornado.web
import tool.decorator as decorator
from core import sqlhelper


class IndexHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @decorator.exception
    def get(self):
        self.render('index.html')

    @decorator.post_exception
    def post(self):
        user = sqlhelper.get_all_record_list('user', {})
        self.ret['data']['name'] = user['username']
        self.ret['data']['profile'] = user['profile']

