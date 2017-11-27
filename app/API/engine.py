# -*- coding: utf-8 -*-

from time import sleep
from random import random

class Engine():

    def rest(self,a,b):
        self.rsleep()
        return str(a-b)

    def sum(self,a,b):
        self.rsleep()
        return str(a+b)

    def test(self, time):
        time = time[0]
        self.rsleep(time)
        return "awake"

    def rsleep(self, *time):
        sleepTime = int(time[0]) if time else random() * 3
        sleep(sleepTime)
