"""
Base Sender

.. todo::  zope.interface or abc

"""
from __future__ import print_function
from __future__ import absolute_import


#import multiprocessing
import threading
import abc  # from zope.interface import implements


class BaseSender(object):

    __metaclass__ = abc.ABCMeta

#    lock = multiprocessing.Lock()
    lock = threading.Lock()

    def send(self, data):
        with self.lock:
            self._send(data)

    @abc.abstractmethod
    def _send(self, data):
        """ implements method """