from __future__ import print_function
from __future__ import absolute_import


from tornado import httpserver
from tornado import ioloop
from tornado.web import StaticFileHandler


from celerymon.web import Site


from .base import BasePlugin
from ..receivers.base import baseHandler


class MuninPlugin(BasePlugin):
    """ Plugin for Munin. Receiver. """

    def __init__(self, host, port, **kwargs):
        super(MuninPlugin, self).__init__(**kwargs)
        self.host = host
        self.port = port
        self.receiver = baseHandler

    def pop_event(self):
        """ Get event tracking data. """
        return self.storage.event("munin")

    def running(self):
        """ Implements method """

    def run(self):
        """ implements method """
        site = Site([(r"", [(r"/$", self.receiver(self))])])

        http_server = httpserver.HTTPServer(site)
        http_server.listen(self.port, address=self.host)
        ioloop.IOLoop.instance().start()

    def logging(self, event):
        """ output """
        self._logging(event and event["workers_average"])
        self._logging(event and event["tasks_average"])
        if self.verbose > 0:
            self._logging(event, "debug")

    def _logging(self, event, level="info"):
        logger = getattr(self.logger, level)
        logger("MuninPlugin/%s:%s tag: %s event: %r " % (
            self.host, self.port, self.tag, event))


