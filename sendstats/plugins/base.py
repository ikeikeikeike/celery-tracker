"""
Base Plugin

.. todo::  zope.interface or abc

"""
from __future__ import print_function
from __future__ import absolute_import


import time
import threading
import abc   # from zope.interface import implements


class BaseThread(threading.Thread):
    """ Base Class """

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(BaseThread, self).__init__(**kwargs)
        self._interval = 10
        self.setDaemon(True)

    def run(self):
        while True:
            self.send()
            time.sleep(self._interval)

    @abc.abstractmethod
    def send(self, data):
        """ implements method """
