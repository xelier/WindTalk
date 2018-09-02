#coding:utf-8
"""
logging封装
"""
import logging
import tornado.options

logging.basicConfig(level=logging.INFO,
                                format='[%(levelname)s %(asctime)s]:%(message)s',
                                datefmt  = '%m-%d %H:%M:%S'
                                )

def debug(msg, *args, **kwargs):
    """
    logging.debug
    """
    if msg:
        currentPort = tornado.options.options.as_dict().get('port', 0)
        logging.debug("[port %s] " % currentPort + msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """
    logging.info
    """
    if msg:
        currentPort = tornado.options.options.as_dict().get('port', 0)
        logging.info("[port %s] " % currentPort + msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    """
    logging.warning
    """
    if msg:
        currentPort = tornado.options.options.as_dict().get('port', 0)
        logging.warning("[port %s] " % currentPort + msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """
    logging.error
    """
    if msg:
        currentPort = tornado.options.options.as_dict().get('port', 0)
        logging.error("[port %s] " % currentPort + msg, *args, **kwargs)