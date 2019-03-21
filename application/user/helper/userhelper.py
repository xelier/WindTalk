# coding:utf-8

from core import sqlhelper
from application.user.dao import userDao
from tool import encrypt


def login(username, password, role):
    """login method"""
    ret = sqlhelper.get_record_by_param('USER', {'USERNAME': username, 'ROLE': role})
    return encrypt.validate_password(ret['PASSWORD'], password)


def register(param):
    """
    It is necessary to check the username's existing before insert a record to table user.
    """
    user_model = {'ID': sqlhelper.generate_id_by_sequence_name("USER_ID_SEQ"), 'USERNAME': param['USERNAME'],
                  'PASSWORD': encrypt.encrypt_password(param['PASSWORD']), 'NICKNAME': param['NICKNAME'], 'ROLE': param['ROLE'],
                  'EMAIL': param['EMAIL']}
    ret = userDao.query_user_info_by_name(user_model['USERNAME'])
    if not ret:
        userDao.add_user(user_model)
        return True
    return False


def modify(param):
    """check the user's existence before update"""
    user_model = {'ID': param['ID'], 'USERNAME': param['USERNAME'],
                  'NICKNAME': param['NICKNAME'], 'ROLE': param['ROLE'],
                  'EMAIL': param['EMAIL']}
    ret = userDao.query_user_info_by_name(user_model['USERNAME'])
    if ret:
        userDao.update_user_info(user_model)
        return True
    return False


def modify_pwd(param):
    """check the user's existence before update"""
    ret = userDao.query_user_info(param['ID'])
    origin_pwd = encrypt.encrypt_password(param['ORIGIN_PASSWORD'], salt=ret['PASSWORD'][:8])
    if ret and encrypt.validate_password(ret['PASSWORD'], origin_pwd):
        user_model = {'ID': param['ID'], 'PASSWORD': encrypt.encrypt_password(param['PASSWORD'])}
        userDao.update_pwd(user_model)
        return True
    return False


def query_user_info(param):
    """query user info"""
    user_id = param['ID']
    return query_user_info(user_id)
