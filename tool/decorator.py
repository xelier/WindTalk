#coding:utf-8

import json
import traceback

from tool import log


def exception(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            log.info(traceback.print_exc())
        finally:
            pass
    return wrapper
