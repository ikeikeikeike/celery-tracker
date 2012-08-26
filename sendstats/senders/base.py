"""
Base Sender

.. todo::  zope.interface or abc

"""
from __future__ import print_function
from __future__ import absolute_import


import threading
import abc  # from zope.interface import implements


class BaseSender(object):

    __metaclass__ = abc.ABCMeta

    lock = threading.Lock()
    socket = None
    verbose = False

    def sending(self, data):
        self.lock.acquire()
        try:
            self.send(data)
        finally:
            self.lock.release()

    @abc.abstractmethod
    def send(self, data):
        """ implements method """