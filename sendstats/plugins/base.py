"""
Base Plugin

.. todo::  zope.interface or abc

"""
from __future__ import print_function
from __future__ import absolute_import


import multiprocessing
import threading
import time
import abc   # from zope.interface import implements


from ..tracking import state


_INTERVAL = 10


#class BasePlugin(threading.Thread):
class BasePlugin(multiprocessing.Process):
    """ Base Class """

    __metaclass__ = abc.ABCMeta

    def __init__(self, logger, interval=_INTERVAL, **kwargs):
        super(BasePlugin, self).__init__(**kwargs)

        self._interval = interval
        self.daemon = True
        self.logger = logger
        self.state = state

    def run(self):
        while True:
            self.send()
            time.sleep(self._interval)

    @abc.abstractmethod
    def send(self):
        """ implements method """
