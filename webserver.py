# ecoding:utf-8
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8888, help='Running in given port', type=int)

