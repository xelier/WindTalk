#encoding:utf-8
import json

import tornado.web
import tool.decorator as decorator
from core import sqlhelper


class IndexHandler(tornado.web.RequestHandler):
    # something should be shown while step into the home page
    # but now I didn't decide what things to show there
    @decorator.exception
    def get(self):
        self.render('index.html')

    @decorator.post_exception
    def post(self):
        user = sqlhelper.get_all_record_list('user', {})
        res = []
        userInfo = {}
        for us in user:
            userInfo['username'] = us['username']
            userInfo['profile'] = us['profile']
            res.append(userInfo)
        self.ret['data'] = res

class LoginHandler(tornado.web.RequestHandler):
    @decorator.post_exception
    @tornado.web.authenticated
    def post(self):
        jsonData = json.loads(self.request.body)

