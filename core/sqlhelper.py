#coding:utf-8
"""
connect to mysql database
"""
import sys
import log
import pymysql
import config.config as config

global pool
pool = None

def connDatabase():
    global pool
    if pool is None:
        log.info('connect database')
        pool = pymysql.connect(host=config.db_host, user=config.db_user, passwd=config.db_pwd, db=config.db_name,
                               port=config.db_port, charset='utf8')
    if not pool:
        log.info("connect failed")
    return pool


def execute(query, ExecuteNoQuery=False, dictCursor=False):
    """
    Basic method to execute the query string.
    @ExecuteNoQuery parameter shows whether we need the returned value. False by default which means the results will be returned.
    """
    conn = connDatabase()
    if dictCursor:
        cur = conn.cursor(cursorclass=pymysql.cursors.DictCursor)
    else:
        cur = conn.cursor()
    ret = None
    try:
        if config.DEBUG:
            print('Execute SQL query: %s' % query)
        count = cur.execute(query)
        if ExecuteNoQuery:
            conn.commit()
            ret = count
        else:
            ret = cur.fetchmany(count)
            # conn.commit()
    except Exception as e:
        log.info('Error when execute SQL string. Exception: %s' % e)
    finally:
        cur.close()
        conn.close()
    return ret


if __name__ == "__main__":
    execute("insert into user values(null ,'bob','bob',1,'bob','xx')")

