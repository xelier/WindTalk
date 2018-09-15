# coding:utf-8
"""
server中用到的公用方法
"""
import os
import re
import urllib
import time
import random
import socket
import datetime
import tool.mymail as mail
import json
import base64
import hashlib

import log
import config.config as config


def retryUntilPass(msg, func, timeout, interval=2, ignoreex=True):
    """
    循环执行指定的函数，直到不出现异常
    """
    result = False
    start = time.mktime(time.localtime())
    print(msg)
    while True:
        if time.mktime(time.localtime()) - start <= timeout:
            try:
                if func():
                    result = True
                    break
            except Exception as e:
                msg = str(e)
                if ignoreex:
                    print('Exception got: %s. Retrying..' % msg)
                else:
                    if hasattr(ignoreex, "__call__"):
                        if ignoreex(msg):
                            print('Exception got: %s. Retrying..' % msg)
                        else:
                            raise e
            time.sleep(interval)
        else:
            print('Function did not succeed within %s seconds.' % timeout)
            break
    return result


def retryUntilValid(msg, func, validate, timeout, interval=10, ignoreex=True):
    """
    Looping execute the function specified by func param and validate the result by validate function within timeout seconds and ignore exception if ignoreex is set to True. \n
    Comment: The ignoreex can also be a function obj to specify an action and throw/ignore the exception accroding to the function result. If the function returns true, then ignore such exceptions, or raise them.
    """
    result = None
    start = time.mktime(time.localtime())
    print(msg)
    while True:
        if time.mktime(time.localtime()) - start <= timeout:
            try:
                ret = func()
                if validate(ret):
                    result = ret
                    break
            except Exception as e:
                msg = str(e)
                if ignoreex:
                    print(e)
                else:
                    if hasattr(ignoreex, "__call__"):
                        if ignoreex(msg):
                            print(e)
                        else:
                            raise e
            time.sleep(interval)
        else:
            print('Function did not succeed within %s seconds.' % timeout)
            break

    return result


def ignoreException(func):
    """
    Execute the function without throwing exceptions if exists.
    """
    try:
        func()
        return True
    except Exception as ex:
        print(ex)
        return False


def current_time_numstr():
    """
    当前时间数字字符串
    """
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def current_datetime():
    """
    当前时间格式化字符串
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def randstr(length, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'):
    """Return a string made up of random chars from alphabet."""
    return ''.join(random.choice(alphabet) for _ in range(length))


def str_md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()


def save_image(image, name, sign_id):
    curDir = os.path.split(os.path.abspath(__file__))[0]
    server_path = os.path.split(curDir)[0]
    folderPath = os.path.join(server_path, 'static', 'sign_succ_images', str(sign_id))
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)
    filePath = os.path.join(folderPath, name + '_' + current_datetime() + '.jpg')
    file = open(filePath, 'wb')
    file.write(base64.b64decode(image))
    file.close()


if __name__ == "__main__":
    # print current_datetime()
    print(str_md5('123456'))

