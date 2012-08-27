"""
Base Plugin

.. todo::  zope.interface or abc

"""
from __future__ import print_function
from __future__ import absolute_import


#import multiprocessing
import threading
import time
import abc   # from zope.interface import implements


from ..tracking import state


# Variables
_INTERVAL = 60
_VERBOSE = False


#class BasePlugin(multiprocessing.Process):
class BasePlugin(threading.Thread):
    """ Base Class """

    __metaclass__ = abc.ABCMeta

    def __init__(self, logger, verbose=_VERBOSE, interval=_INTERVAL, **kwargs):
        super(BasePlugin, self).__init__(**kwargs)

        self.interval = interval
        self.verbose = verbose
        self.logger = logger
        self.daemon = True
        self.state = state

    def run(self):
        while True:
            self.send()
            time.sleep(self.interval)

    @abc.abstractmethod
    def send(self):
        """ implements method """