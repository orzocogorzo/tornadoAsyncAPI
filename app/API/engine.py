# -*- coding: utf-8 -*-

from time import sleep
from multiprocessing import Pool, Process
from random import random
from math import floor

class Engine():

    def rest(self,a,b):
        self.rsleep()
        return str(a-b)

    def sum(self,a,b):
        self.rsleep()
        return str(a+b)

    def test(self):
        self.rsleep()
        return "awake"

    def rsleep(self):
        time = random() * 3
        sleep(time)
