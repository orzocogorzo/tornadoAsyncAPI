# -*- coding: utf-8 -*-

import os
import logging
import datetime as dt
from functools import wraps

class Logger():
    def __init__(self, name, level, logfile):
        self.name = name
        self.level = level
        self.file = os.path.abspath(logfile)
        self.logger = None

        self.start()

    def setup_handler(self):
        try:
            self.handler = logging.FileHandler(self.file)

            if self.level.lower() == 'info':
                self.handler.setLevel(logging.INFO)
            elif self.level.lower() == 'error':
                self.handler.setLevel(logging.ERROR)
            elif self.level.lower() == 'debug':
                self.handler.setLevel(logging.DEBUG)
            else:
                print "Can't indentify logger level"

            self.logger.addHandler(self.handler)

        except ValueError:
            print "Log File Handlers doesn't exist"

    def start(self):
        try:
            self.logger = logging.getLogger(self.name)

            if self.level.lower() == 'info':
                self.logger.setLevel(logging.INFO)
            elif self.level.lower() == 'error':
                self.logger.setLevel(logging.ERROR)
            elif self.level.lower() == 'debug':
                self.logger.setLevel(logging.DEBUG)
            else:
                print "Can't indentify logger level"

            self.setup_handler()
            self.log_init()

        except ValueError:
            print 'Something went wrong on logger setup process'

    def log_init(self):
        self.logger.info('session started at {}'.format(dt.datetime.now().strftime('%Y-%m%-d %H:%M:%S')))

    def log_start(self):
        start = dt.datetime.now()
        self.logger.info('start time: %s', start.strftime('%Y-%m%-d %H:%M:%S'))
        return start

    def log_end(self, start):
        end = dt.datetime.now()
        delta = end - start
        self.logger.info('end task at %s. Delta time is %s', end.strftime('%Y-%m%-d %H:%M:%S'), delta)

    def track(self, func):
        this = self
        @wraps(func)
        def func_wrapper(handler):
            start = this.log_start()
            result = func(handler)
            this.log_end(start)
            return result

        return func_wrapper
