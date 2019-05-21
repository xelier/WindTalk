from core import sqlhelper


def add_comment(param):
    return sqlhelper.insert_record("COMMENT", param)


def delete_comment(comment_id):
    return sqlhelper.delete_record_by_param("COMMENT", {'COMMENT_ID': comment_id})


def query_comment_list(article_id):
    return sqlhelper.get_all_record_list('COMMENT', {'ARTICLE_ID': article_id})


def query_comment_page_list(param):
    return sqlhelper.get_page_list('COMMENT', param['CONDITION'], int(param['PAGE_INDEX']), int(param['PAGE_SIZE']), field_list=param['FIELDS'])


def query_comment_list_count(param):
    """query article info count"""
    ret = {'RECORD_NUM': sqlhelper.get_all_record_num('COMMENT', param['CONDITION']),
           'PAGE_COUNT': sqlhelper.get_page_num('COMMENT', param['CONDITION'], int(param['PAGE_SIZE']))}
    return ret
