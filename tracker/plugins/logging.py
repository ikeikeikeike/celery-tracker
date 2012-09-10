"""
Logging Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BasePlugin


class LoggingPlugin(BasePlugin):

    def __init__(self, **kwargs):
        super(LoggingPlugin, self).__init__(**kwargs)

    def running(self):
        """ implements method """
        if self.verbose:
            self.logger.debug(
                "LoggingPlugin: (host)%s:%s, (tag)%s, (data)%r " % (
                    "localhost", "none", "logging", {}))
