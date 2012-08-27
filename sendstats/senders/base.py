"""
Base Sender

.. todo::  zope.interface or abc

"""
from __future__ import print_function
from __future__ import absolute_import


import threading
#import multiprocessing
import abc  # from zope.interface import implements


class BaseSender(object):

    __metaclass__ = abc.ABCMeta

    lock = threading.Lock()
#    lock = multiprocessing.Lock()

    def send(self, data):
        self.lock.acquire()
        try:
            self._send(data)
        finally:
            self.lock.release()

    @abc.abstractmethod
    def _send(self, data):
        """ implements method """