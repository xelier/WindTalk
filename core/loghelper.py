# coding:utf-8
import datetime

from core import sqlhelper


def add_log_record(ip, req_item, user=None):
    """
    添加访问记录
    :param ip:
    :param req_item:
    :param user:
    :return:
    """
    if ip == '::1' or ip == '127.0.0.1':
        return None
    insert_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {'IP_HOST': ip, 'INTERFACE_NAME': req_item, 'TIME': insert_time}
    if user:
        record['ID'] = user
    result = sqlhelper.insert_record('op_log', record)
    return result

