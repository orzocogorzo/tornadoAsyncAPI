# -*- coding: utf-8 -*-

from os import path

import tornado
from tornado import gen, ioloop, httpserver
from tornado.web import Application, RequestHandler, asynchronous

from gevent import spawn
from gevent.queue import Queue

from engine import Engine
from logger import Logger
from utils import Utils

#app configuration
from config.config import settings


#HELPERS
logPath = path.abspath(path.join(path.dirname(__file__), "logs/info.log"))
lg = Logger(name=__name__, level=settings['loglevel'], logfile=logPath)
ut = Utils()

#ENGINE INSTANCE
engine = Engine()


#RequestHandlers
class MainHandler(RequestHandler):
    def get(self):
        self.write("Welcome to the API")

class SumHandler(RequestHandler):
    @gen.coroutine
    @lg.track
    def get(self):
        data = ut.serializeData(self, {'a': int, 'b': int})
        response = self.engineRequest(**data)
        self.write(response)
        self.finish()

    def engineRequest(self, **data):
        result = spawn(engine.sum, data['a'], data['b'])
        result.run()
        response = result.get()
        return response

class RestHandler(RequestHandler):
    @gen.coroutine
    @lg.track
    def get(self):
        data = ut.serializeData(self, {'a': int, 'b': int})
        result = self.engineRequest(**data)
        self.write(result.result())
        self.finish()

    @asynchronous
    def engineRequest(self, **data):
        result = engine.rest(a=data['a'], b=data['b'])
        raise gen.Return(result)

class TestHandler(RequestHandler):
    @gen.coroutine
    @lg.track
    def get(self):
        result = yield self.engineRequest()
        self.write(result)
        self.finish()

    @gen.coroutine
    def engineRequest(self, **data):
        result = engine.test()
        raise gen.Return(result)

# APP ROUTES
routes = [
    (r"/", MainHandler),
    (r"/sum", SumHandler),
    (r"/rest", RestHandler),
    (r"/test", TestHandler),
]


#APP INITIALIZER
def main():
    app = tornado.web.Application(routes, **settings)
    http_server = httpserver.HTTPServer(app)
    http_server.bind(5000)
    http_server.start(0)
    #http_server.listen(5000)
    print "server listening to 127.0.0.1:5000"
    #ioloop.IOLoop.instance().start()
    ioloop.IOLoop.current().start()
