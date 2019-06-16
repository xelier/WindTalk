# coding:utf-8

from core import sqlhelper
from application.user.dao import userDao
from tool import encrypt


def login(username, password, role):
    """login method"""
    ret = sqlhelper.get_record_by_param('USER', {'USERNAME': username, 'ROLE': role})
    if ret is not None:
        if encrypt.validate_password(ret['PASSWORD'], password):
            return ret
    return False


def register(param):
    """
    It is necessary to check the username's existing before insert a record to table user.
    """
    user_model = {'USERNAME': param['USERNAME'],
                  'PASSWORD': encrypt.encrypt_password(param['PASSWORD']), 'NICKNAME': param['NICKNAME'], 'ROLE': param['ROLE'],
                  'EMAIL': param['EMAIL']}
    ret = userDao.query_user_info_by_name(user_model['USERNAME'])
    if not ret:
        user_model['ID'] = sqlhelper.generate_id_by_sequence_name("USER_ID_SEQ")
        userDao.add_user(user_model)
        return user_model
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


def query_user_list(param):
    article_param = {'CONDITION': param['CONDITION'], 'PAGE_INDEX': param['PAGE_INDEX'],
                     'PAGE_SIZE': param['PAGE_SIZE'],
                     'FIELDS': ['ID', 'USERNAME', 'NICKNAME', 'ROLE', 'EMAIL']}
    article_list = userDao.query_user_list(article_param)
    article_page_info = userDao.query_user_list_count(article_param)
    ret = {'RESULT_LIST': article_list, 'RECORD_NUM': article_page_info['RECORD_NUM'],
           'PAGE_COUNT': article_page_info['PAGE_COUNT']}
    return ret


def detele_user(param):
    """
        Delete An Article.
        """
    if param['USER_ID']:
        userDao.delete_user(param['USER_ID'])
        return True
    return False
