#coding: utf-8

MAX_BUFFER_SIZE = 200 * 1024 * 1024

DEBUG = True
if DEBUG:
    db_name = 'forfundb'
    db_user = 'forfun'
    db_pwd = 'xelier'
    db_port = 3306
    # db_host = '119.29.35.83'
    db_host = 'localhost'
else:
    db_name = 'forfundb'
    db_user = 'forfun'
    db_pwd = 'xelier'
    db_port = 3306
    db_host = '119.29.35.83'
