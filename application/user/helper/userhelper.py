# coding:utf-8
import base64

from core import sqlhelper
from application.user.dao import userDao


def login(username, password, role):
    """login method"""
    ret = sqlhelper.get_record_by_param('user', {'username': username, 'password': password, 'role': role})
    if ret:
        return ret['username']
    return None


def register(param, user_model=None):
    """
    It is necessary to check the username's existing before insert a record to table user.
    """
    user_model['ID'] = sqlhelper.generate_id_by_sequence_name("USER_ID_SEQ")
    user_model['USERNAME'] = param['USERNAME']
    user_model['PASSWORD'] = param['PASSWORD']
    user_model['NICKNAME'] = param['NICKNAME']
    user_model['ROLE'] = param['ROLE']
    user_model['EMAIL'] = param['EMAIL']
    ret = userDao.query_user_info_by_name(user_model['USERNAME'])
    if ret:
        return False
    else:
        userDao.add_user(user_model)
        return True


def modify(param, user_model=None):
    user_model['ID'] = sqlhelper.generate_id_by_sequence_name("USER_ID_SEQ")
    user_model['USERNAME'] = param['USERNAME']
    user_model['PASSWORD'] = param['PASSWORD']
    user_model['NICKNAME'] = param['NICKNAME']
    user_model['ROLE'] = param['ROLE']
    user_model['EMAIL'] = param['EMAIL']
    ret = userDao.query_user_info_by_name(user_model['USERNAME'])
    if ret:
        userDao.update_user_info(user_model)
        return True
    else:
        return False
