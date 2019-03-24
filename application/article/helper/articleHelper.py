# coding:utf-8
import datetime

from core import sqlhelper
from application.article.dao import articleDao


def add(param):
    """add an article"""
    article_param = {'CONTENT': param['CONTENT'], 'CREATE_TIME': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'TITLE': param['TITLE'], 'CREATE_USER': param['ID'],
                     'DESCRIPTION': param['CONTENT'][:200]+'...' if len(param['CONTENT']) > 200 else param['CONTENT']+'...'}
    ret = sqlhelper.get_record_by_param('ARTICLE', {'TITLE': param['TITLE']})
    if not ret:
        article_param['ARTICLE_ID'] = sqlhelper.generate_id_by_sequence_name('ARTICLE_ID_SEQ')
        articleDao.add_article(article_param)
        return article_param['ARTICLE_ID']
    return False


def delete(param):
    """
    Delete An Article.
    """
    if param['ARTICLE_ID']:
        articleDao.delete_article(param['ARTICLE_ID'])
        return True
    return False


def modify(param):
    """check the article's existence before update"""
    article_param = {'CONTENT': param['CONTENT'], 'CREATE_TIME': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'TITLE': param['TITLE'], 'CREATE_USER': param['ID'],
                     'DESCRIPTION': param['CONTENT'][:200] + '...' if len(param['CONTENT']) > 200 else param['CONTENT'] + '...',
                     'ARTICLE_ID': param['ARTICLE_ID']
                     }
    ret = sqlhelper.get_record_by_param('ARTICLE', article_param['ARTICLE_ID'])
    if ret:
        articleDao.edit_article(article_param)
        return True
    return False


def query_list(param):
    """add necessary param to the article's list"""
    article_param = {'CONDITION': param['CONDITION'], 'PAGE_INDEX': param['PAGE_INDEX'], 'PAGE_SIZE': param['PAGE_SIZE'],
                     'FIELDS': ['ARTICLE_ID', 'TITLE', 'DESCRIPTION', 'CREATE_USER', 'CREATE_USER']}
    article_list = articleDao.query_article_list(article_param)
    article_page_info = articleDao.query_article_list_count(article_param)
    ret = {'RESULT_LIST': article_list, 'RECORD_NUM': article_page_info['RECORD_NUM'], 'PAGE_COUNT':article_page_info['PAGE_COUNT']}
    return ret


def query_info(param):
    """query article info"""
    article_id = param['ARTICLE_ID']
    return articleDao.query_article_info(article_id)
