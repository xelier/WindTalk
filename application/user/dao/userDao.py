from core import sqlhelper


def add_user(param):
    """add a user"""
    return sqlhelper.insert_record("USER", param)


def delete_user(user_id):
    """delete a user"""
    return sqlhelper.delete_record_by_param('USER', {'ID': user_id})


def update_pwd(param):
    """update password"""
    return sqlhelper.update_table('USER', {'ID': param['ID']}, {'PASSWORD': param['PASSWORD']})


def update_user_info(param):
    """get user password"""
    # update_param = param
    # del update_param['ID']
    return sqlhelper.update_table('USER', {'ID': param['ID']}, param)


def query_user_info(user_id):
    """query user information"""
    return sqlhelper.get_record_by_param('USER', {'ID': user_id})


def query_user_info_by_name(user_name):
    """query user information"""
    return sqlhelper.get_record_by_param('USER', {'USERNAME': user_name})


def query_user_list(param):
    """query user information"""
    return sqlhelper.get_page_list('USER', param['CONDITION'], int(param['PAGE_INDEX']), int(param['PAGE_SIZE']), field_list=param['FIELDS'])


def query_user_list_count(param):
    """query user information"""
    ret = {'RECORD_NUM': sqlhelper.get_all_record_num('USER', param['CONDITION']),
           'PAGE_COUNT': sqlhelper.get_page_num('USER', param['CONDITION'], int(param['PAGE_SIZE']))}
    return ret


