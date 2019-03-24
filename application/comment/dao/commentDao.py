from core import sqlhelper


def add_comment(param):
    return sqlhelper.insert_record("COMMENT", param)


def delete_comment(comment_id):
    return sqlhelper.delete_record_by_param("COMMENT", {'COMMENT_ID': comment_id})


def query_comment_list(article_id):
    return sqlhelper.get_all_record_list('COMMENT', {'ARTICLE_ID': article_id})


