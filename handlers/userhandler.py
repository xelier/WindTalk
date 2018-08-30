#encoding:utf-8
import tornado


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'hello')
        self.write(greeting + ', friendly user!')
