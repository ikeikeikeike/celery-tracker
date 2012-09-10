"""
Fluent Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BasePlugin
from ..senders.fluent import FluentSender


class FluentPlugin(BasePlugin):
    """ Plugin for Fluent. """

    def __init__(self, host, port, **kwargs):
        """

        @see celeryconfig.CELERY_TRACKER_PLUGINS.

        :param str host: Host name.
        :param int port: Port number.
        """
        super(FluentPlugin, self).__init__(**kwargs)

        self.host = host
        self.port = port
        self.sender = FluentSender(
            tag=self.tag, host=self.host, port=self.port)

    def pop_event(self):
        """ Get event tracking data. """
        return self.storage.event("fluent")

    def running(self):
        """ implements method """
        event = self.pop_event()

        workers_average = event and event["workers_average"]
        self.sender.send(workers_average)

        tasks_average = event and event["tasks_average"]
        self.sender.send(tasks_average)

        self._logging(workers_average)
        self._logging(tasks_average)
        if self.verbose > 0:
            self._logging(event, "debug")

    def _logging(self, event, level="info"):
        logger = getattr(self.logger, level)
        logger("FluentPlugin/%s:%s tag: %s event: %r " % (
            self.host, self.port, self.tag, event))
