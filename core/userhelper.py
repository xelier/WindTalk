# coding:utf-8
from core import sqlhelper


def login(username, password, role):
    """
    this is the fucking login method
    """
    ret = sqlhelper.get_record_by_param('user', {'username': username, 'password': password, 'role': role})
    if ret:
        return ret['username']
    return False


def register(username, password, role, sex, nickname, profile):
    """
    this is the fucking register method
    It is necessary to check the username's existing before insert a record to table user.
    """
    ret = sqlhelper.get_record_by_param('user', {'username': username})
    if ret:
        return True
    else:
        sqlhelper.insert_record('user', {'username': username, 'password': password, 'role': role, 'sex': sex, 'nickname': nickname, 'profile': profile})

