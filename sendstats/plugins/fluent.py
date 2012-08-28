"""
Fluent Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BasePlugin
from ..senders.fluent import FluentSender


class FluentPlugin(BasePlugin):

    def __init__(self, host, port, **kwargs):
        super(FluentPlugin, self).__init__(**kwargs)

        self.host = host
        self.port = port
        self.sender = FluentSender(
            tag=self.tag, host=self.host, port=self.port)

    def send(self):
        """ implements method """
        for data in self.storage.event("fluent"):
            if self.verbose:
                self.logger.debug(
                    "FluentPlugin: (host)%s:%s, (tag)%s, (data)%r " % (
                        self.host, self.port, self.tag, data))
            self.sender.send(data)