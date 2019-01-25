#coding:utf-8
"""
connect to mysql database
"""
import tool.log as log
import pymysql
import config.config as config
from DBUtils.PooledDB import PooledDB

global pool
pool = None


def connDatabase():
    global pool
    if pool is None:
        print('connect database')
        pool = PooledDB(creator=pymysql,
                        maxconnections=None,
                        mincached=2,
                        maxcached=5,
                        maxshared=0,
                        blocking=True,
                        maxusage=None,
                        setsession=[],
                        ping=0,
                        host=config.db_host,
                        port=config.db_port,
                        user=config.db_user,
                        passwd=config.db_pwd,
                        db=config.db_name,
                        charset='utf8'
                        )
    if not pool:
        log.info("connect failed")
    return pool.connection()


def execute(query, ExecuteNoQuery=False, dictCursor=False):
    """
    Basic method to execute the query string.
    @ExecuteNoQuery parameter shows whether we need the returned value. False by default which means the results will be returned.
    """
    conn = connDatabase()
    if dictCursor:
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
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
    # batchCount是字段长度，
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
        log.info('Error when execute SQL string. Exception: %s' % e)
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


def update_table(table, conditionDict, updateDict):
    """
    更新table
    @updateDict:更新数据
    @conditionDict:参数字典，唯一确定记录
    """
    ret = True
    sql = "update %s set " % table
    for key, val in updateDict.items():
        if isinstance(val, int):
            sql += "%s = '%d'," % (key, val)
        elif isinstance(val, float):
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
            sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
    sql = sql[:-5]
    result = execute(sql, ExecuteNoQuery=True)
    if result is None:
        ret = False
    return ret


def get_record_by_param(table, paramDict):
    """
    参数查询
    @paramDict：查询参数
    """
    ret = None
    sql = "select * from %s where " % table
    for key, val in paramDict.items():
        sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
    sql = sql[:-5]
    result = execute(sql, dictCursor=True)
    if result is not None and len(result) > 0:
        ret = result[0]
    return ret


def get_fields_value(table, paramDict, * args):
    """
    查询某些字段，通常参数唯一确定某条记录
    @paramDict：查询参数
    @args: 要查询的字段，元组
    返回字典
    """
    ret = {}
    sql = "select * from %s where " % table
    for key, val in paramDict.items():
        sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
    sql = sql[:-5]
    result = execute(sql, dictCursor=True)
    if result is None or len(result) == 0:
        return None
    for field in args:
        ret[field] = result[0][field]
    return ret


def get_field_value(table, paramDict, fieldName):
    """
    查询某些字段，通常参数唯一确定某条记录
    @paramDict：查询参数
    @args: 要查询的字段，元组
    返回字典
    """
    sql = "select * from %s where " % table
    for key, val in paramDict.items():
        sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
    sql = sql[:-5]
    result = execute(sql, dictCursor=True)
    if result is None or len(result) == 0:
        return None
    return result[0][fieldName]


def delete_record_by_param(table, paramDict):
    """
    删除记录
    @paramDict：查询参数
    """
    sql = "delete from %s where " % table
    for key, val in paramDict.items():
        sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
    sql = sql[:-5]  # 过滤最后两个空格和‘and’
    result = execute(sql, ExecuteNoQuery=True)

    if result is None:
        return False
    return True


def get_all_record_list(table, paramDict ):
    """
    查询所有数据
    :param table:
    :param paramDict:
    :param pageid:
    :param pagesize:
    :return:
    """
    sql = "select * from %s " % table
    if paramDict is not None and len(paramDict) > 0:
        sql += "where "
        for key, val in paramDict.items():
            sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
        sql = sql[:-5]
    result = execute(sql, dictCursor=True)
    return result


def get_all_record_num(table, paramDict):
    """
    查询所有数据条数
    :param table:
    :param paramDict:
    :param pagesize:
    :return:
    """
    sql = "select count(*) pagenum from %s " % table
    if paramDict is not None and len(paramDict) > 0:
        sql += "where "
        for key, val in paramDict.items():
            sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
        sql = sql[:-5]
    result = execute(sql, dictCursor=True)
    ret = int(result[0]['pagenum'])
    return int(ret)


def get_page_list(table, paramDict, pageid, pagesize):
    """
    分页查询
    :param table:
    :param paramDict:
    :param pageid:
    :param pagesize:
    :return:
    """
    sql = "select * from %s " % table
    if paramDict is not None and len(paramDict) > 0:
        sql += "where "
        for key, val in paramDict.items():
            sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
        sql = sql[:-5]
    sql += " limit %d, %d" % (pageid*pagesize, pagesize)
    result = execute(sql, dictCursor=True)
    return list(result)


def get_page_num(table, paramDict, pagesize):
    """
    查询有多少页
    :param table:
    :param paramDict:
    :param pagesize:
    :return:
    """
    sql = "select count(*) pagenum from %s " % table
    if paramDict is not None and len(paramDict) > 0:
        sql += "where "
        for key, val in paramDict.items():
            sql += "%s = '%s' and " % (key, pymysql.escape_string(val))
        sql = sql[:-5]
    result = execute(sql, dictCursor=True)
    ret = int(result[0]['pagenum'])
    if ret % pagesize > 0:
        ret = ret/pagesize + 1
    else:
        ret = ret/pagesize
    return int(ret)






if __name__ == "__main__":
    insert_record('user', {'username': 'bob', 'password': 'bob', 'sex': 0, 'nickname': '中文', 'profile': 'xxx'})
    # update_table('user', {'username': 'bob'}, {'nickname': '继续'})
    # s = get_record_by_param('user', {'username': 'bob'})

    # s = get_fields_value('user', {'username': 'bob'}, 'password', 'profile')
    # s = get_field_value('user', {'username': 'bob'}, 'password')
    # s = delete_record_by_param('user', {'username': 'bob'})
    # s = get_page_list('user', {}, 0, 100)
    # s = get_page_num('user', {'username': 'bob'}, 100)
    # s = get_all_record_num('user', {'username': 'xelier'})
    # execute("insert into user values(null ,'bob','bob',1,'bob','xx')")
    # delete_record_by_param("user", {'userName': 'bob'})
    # print(s)
    # pass

