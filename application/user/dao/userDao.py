from core import sqlhelper


def add_user(param):
    """add a user"""
    return sqlhelper.insert_record("USER", param)


def delete_user(user_id):
    """delete a user"""
    return sqlhelper.delete_record_by_param('USER', {'ID': user_id})


def update_pwd(param):
    """update password"""
    return sqlhelper.update_table('USER', {'ID': param['ID']}, {'PASSWORD': param['NEW_PWD']})


def update_user_info(param):
    """get user password"""
    return sqlhelper.update_table('USER', {'ID': param['ID']}, param)


def query_user_info(user_id):
    """query user information"""
    return sqlhelper.get_record_by_param('USER', {'ID': user_id})


