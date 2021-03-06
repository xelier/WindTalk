import datetime

from application.comment.dao import commentDao
from core import sqlhelper


def add(param):
    """add a comment"""
    comment_model = {'ARTICLE_ID': param['ARTICLE_ID'], 'EMAIL': param['EMAIL'], 'CONTENT': param['CONTENT'],
                     'CREATE_TIME':  datetime.datetime.now().strftime("%Y-%m-%d"),
                     'COMMENT_ID': sqlhelper.generate_id_by_sequence_name('COMMENT_ID_SEQ')}
    return commentDao.add_comment(comment_model)


def delete(param):
    """delete a comment"""
    comment_id = param['COMMENT_ID']
    return commentDao.delete_comment(comment_id)


def query_comment_list(param):
    """query comment list"""
    article_id = param['ARTICLE_ID']
    return commentDao.query_comment_list(article_id)


def query_comment_page(param):
    comment_param = {'CONDITION': param['CONDITION'], 'PAGE_INDEX': param['PAGE_INDEX'],
                     'PAGE_SIZE': param['PAGE_SIZE'],
                     'FIELDS': ['ARTICLE_ID', 'COMMENT_ID', 'CONTENT', 'EMAIL']}
    article_list = commentDao.query_comment_page_list(comment_param)
    article_page_info = commentDao.query_comment_list_count(comment_param)
    ret = {'RESULT_LIST': article_list, 'RECORD_NUM': article_page_info['RECORD_NUM'],
           'PAGE_COUNT': article_page_info['PAGE_COUNT']}
    return ret
