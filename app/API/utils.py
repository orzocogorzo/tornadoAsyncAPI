# -*- coding: utf-8 -*-

from functools import wraps
from gevent import spawn
from gevent.queue import Queue

this = None

class Utils():

    def serializeData(self, handler, keys):
        data = {}
        for k, type in keys.items():
            data[k] = type(handler.get_argument(k))
        return data

    def onFinish(self, handler, result):
        handler.write(result)
        handler.finish()

    # DECORATORS
    def gevent_async(self, func):
        global this
        this = self
        @wraps(func)
        def gevent_wrapper(handler):
            handler.response = lambda result: handler.q.put(result)
            handler.q = Queue(1)
            p = spawn(func, handler)
            p.run()
            done = handler.q.get()
            global this
            this.onFinish(handler, done)

        return gevent_wrapper

