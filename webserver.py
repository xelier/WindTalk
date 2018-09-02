# ecoding:utf-8
import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import config.config as _conf
from tornado.options import define, options

from handlers import urlhandler

define("port", default=8888, help='Running in given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = urlhandler.urlhandlers
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "web/template"),
            static_path=os.path.join(os.path.dirname(__file__), "web/static"),
            xsrf_cookies=False,
            debug=True,
            cookie_secret="Ck+z+ODuQ9CeS1XJHN6sYI5mn99x50ZkkLn/WDHclC0="
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    try:
        print("Start cron job background controler.")
    except Exception as e:
        print("Start controler failed: %s" % e)
    tornado.options.parse_command_line()
    httpserver = Application()
    print("Port: ", options.port)
    httpserver.listen(options.port, max_buffer_size=_conf.MAX_BUFFER_SIZE)
    print("Start IOLoop.")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len == 2:
        options.port = int(sys.argv[1])
    main()
