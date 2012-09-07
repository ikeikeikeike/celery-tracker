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


# Variables
_INTERVAL = 300
_VERBOSE = False


#class BasePlugin(multiprocessing.Process):
class BasePlugin(threading.Thread):
    """ Base class for a plugin. """

    __metaclass__ = abc.ABCMeta

    def __init__(self, logger, tag, storage,
                 verbose=_VERBOSE, interval=_INTERVAL, **kwargs):
        """
        initialize

        :param logging logger: Logger object.
        :param str tag: Tag name.
        :param str storage: Path to storage.
        :param int verbose: Increment verbose level (1: debug, 2: trace, 3: debug trace)
        :param str storage: Path to storage.
        """
        super(BasePlugin, self).__init__(**kwargs)

        self.interval = interval
        self.storage = storage
        self.verbose = verbose
        self.logger = logger
        self.daemon = True
        self.tag  = tag

    def run(self):
        """ Runner """
        while True:
            self.send()
            time.sleep(self.interval)

    @abc.abstractmethod
    def send(self):
        """ Implements method """