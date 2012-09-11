from __future__ import print_function
from __future__ import absolute_import


from .base import BaseReceivePlugin


class ReceivePlugin(BaseReceivePlugin):
    """ Plugin for Receiver. """

    def pop_event(self):
        """ Get event tracking data. """
        return self.storage.event("receive")

    def logging(self, event):
        """ output """
        self._logging(event and event["workers_average"])
        self._logging(event and event["tasks_average"])
        if self.verbose > 0:
            self._logging(event, "debug")

    def _logging(self, event, level="info"):
        logger = getattr(self.logger, level)
        logger("ReceivePlugin/%s:%s tag: %s event: %r " % (
            self.host, self.port, self.tag, event))
