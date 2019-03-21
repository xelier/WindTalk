#coding:utf-8
import functools
import json
import traceback

import tornado.web

from core import loghelper
from tool import log, util


def exception(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            log.info(traceback.print_exc())
        finally:
            pass
    return wrapper


class DatetimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(self, o):
            return o.strftime('%Y-%M-%D %H:%M:%S')
        return json.JSONEncoder.default(self, o)


def post_exception(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.ret = {'succ': True, 'err': '', 'data': {}}
        try:
            func(self, *args, **kwargs)
        except tornado.web.MissingArgumentError as e:
            log.info(traceback.format_exc())
            self.ret['succ'] = False
            self.ret['err'] = e if e != '' else e.log_message
        finally:
            self.write(json.dumps(self.ret, cls=DatetimeEncoder))
            util.ignoreException(lambda: loghelper.add_log_record(ip=self.request.remote_ip, req_item=self.__class__.__name__))
    return wrapper


def get_exception(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.ret = {'succ': True, 'err': '', 'data': {}}
        try:
            func(self, *args, **kwargs)
        except tornado.web.MissingArgumentError as e:
            log.info(traceback.format_exc())
            self.ret['succ'] = False
            self.ret['err'] = e if e != '' else e.log_message
        finally:
            self.write(json.dump(self.ret, cls=DatetimeEncoder))
            util.ignoreException(lambda : loghelper.add_log_record(ip=self.request.remote_ip, req_item=self.__class__.__name__))
    return wrapper

