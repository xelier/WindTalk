from core import sqlhelper


def add_article(param):
    """add an article"""
    return sqlhelper.insert_record("ARTICLE", param)


def delete_article(article_id):
    """delete an article"""
    return sqlhelper.delete_record_by_param('ARTICLE', {'ARTICLE_ID': article_id})


def edit_article(param):
    """update articles"""
    return sqlhelper.update_table('ARTICLE', {'ARTICLE_ID': param['ARTICLE_ID']}, param)


def query_article_info(article_id):
    """query article information"""
    return sqlhelper.get_record_by_param('ARTICLE', {'ARTICLE_ID': article_id})


def query_article_list(param):
    """query article information"""
    return sqlhelper.get_page_list('ARTICLE', param['CONDITION'], param['PAGE_INDEX'], param['PAGE_SIZE'], field_list=param['FIELDS'])


def query_article_list_count(param):
    """query article info count"""
    ret = {'RECORD_NUM': sqlhelper.get_all_record_num('ARTICLE', param['CONDITION']),
           'PAGE_COUNT': sqlhelper.get_page_num('ARTICLE', param['CONDITION'], param['PAGE_SIZE'])}
    return ret



