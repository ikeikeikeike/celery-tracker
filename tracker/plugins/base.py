"""
Base Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


#import multiprocessing
import threading
import time
import abc   # from zope.interface import implements


# External
from tornado import httpserver
from tornado import ioloop


# Internal
from .web import Site
from ..receivers.base import baseHandler


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
        self.tag = tag

    def run(self):
        """ Runner """
        while True:
            self.running()
            time.sleep(self.interval)

    @abc.abstractmethod
    def running(self):
        """ Implements method """


class BaseReceivePlugin(BasePlugin):
    """ Base Receiver Class  """

    def __init__(self, host, port, **kwargs):
        """
        initialize

        :param str host: Host address.
        :param int port: Port number.
        """
        super(BaseReceivePlugin, self).__init__(**kwargs)
        self.host = host
        self.port = port
        self.receiver = baseHandler

    def running(self):
        pass

    def logging(self, event):
        pass

    def run(self):
        """ Runner """
        site = Site([(r"", [(r"/$", self.receiver(self))])])

        http_server = httpserver.HTTPServer(site)
        http_server.listen(self.port, address=self.host)
        ioloop.IOLoop.instance().start()

    @abc.abstractmethod
    def pop_event(self):
        """ Implements method, Get event tracking data. """
