import json
from abc import ABC
import tool.decorator as decorator
from application.comment.helper import commentHelper
from application.user.handler.userHandler import BaseHandler


class AddCommentHandler(BaseHandler, ABC):
    @decorator.post_exception
    def post(self):
        json_data = json.dumps(self.request.body)
        ret = commentHelper.add(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Add Article Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Add Comment Failed'


class DeleteCommentHandler(BaseHandler, ABC):
    @decorator.post_exception
    def post(self):
        json_data = json.loads(self.request.body)
        ret = commentHelper.delete(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data']['resultDesc'] = 'Delete Article Successful'
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'Delete Comment Failed'


class QueryCommentListHandler(BaseHandler, ABC):
    @decorator.get_exception
    def get(self):
        json_data = json.loads(self.get_argument("param"))
        ret = commentHelper.query_comment_list(json_data)
        if ret:
            self.ret['succ'] = True
            self.ret['data'] = ret
        else:
            self.ret['succ'] = False
            self.ret['err'] = 'No Comment Found'
