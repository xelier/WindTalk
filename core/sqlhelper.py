#coding:utf-8
"""
connect to mysql database
"""
import sys
import core.log as log
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


def insert_many(sql, valueList):
    """
    Basic method to batch execute the insert string.
    @ExecuteNoQuery parameter shows whether we need the returned value. False by default which means the results will be returned.
    """
    conn = connDatabase()
    cur = conn.cursor()
    ret = None
    # batchCount是字段长度
    batchCount = 10000
    bugCount = len(valueList)
    times = bugCount / batchCount
    times = times + 1 if bugCount % batchCount > 0 else times
    try:
        if config.DEBUG:
            print('Execute SQL query: %s' % sql)
        for i in range(times):
            count = cur.executemany(sql, valueList[i * batchCount: (i + 1) * batchCount])
        conn.commit()
        ret = count
    except Exception as e:
        log.info('Error when execute SQL string. Exception: %s' % e.message)
    finally:
        cur.close()
        conn.close()
    return ret

def insert_record(table, paramDict):
    """
    添加记录
    """
    fields = ""
    vals = ""
    for key, val in paramDict.items():
        fields += key + ","
        vals += pymysql.escape_string(str(val)) + "','"
    fields = fields.strip(",")
    vals = vals[:-3] #strip会过滤掉最后的空字符串值
    sql = "insert into %s (%s) values ('%s')" % (table, fields, vals)
    result = execute(sql, ExecuteNoQuery=True)
    if result is None:
        return False
    return True

def update_table(table,conditionDict,updateDict):
    """
    更新table
    @updateDict:更新数据
    @conditionDict:参数字典，唯一确定记录
    """
    ret = True
    sql = "update %s set" % table
    for key, val in updateDict.items():
        if isinstance(val, int):
            sql += "%s = '%d'," % (key, val)
        elif isinstance(val,float):
            sql += "%s = '%f'," % (key, val)
        else:
            sql += "%s = '%s'," % (key, pymysql.escape_string(val))
    sql = sql.strip(",")
    sql += " where "
    for key, val in conditionDict.items():
        if isinstance(val, int):
            sql += "%s = '%d' and " % (key, val)
        elif isinstance(val, float):
            sql += "%s = '%f' and " % (key, val)
        elif isinstance(val, str):
            val = val.replace("'", "\\'").encode("utf-8")
            sql += "%s='%s' and " % (key, val)
        else:
            sql += "%s = '%s' and " % (key, val.replace("'", "\\'").replace("\\", "\\\\"))
    sql = sql[:-5]
    result = execute(sql, ExecuteNoQuery=True)
    if result is None:
        ret = False
    return ret





if __name__ == "__main__":
    execute("insert into user values(null ,'bob','bob',1,'bob','xx')")



