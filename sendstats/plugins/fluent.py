"""
Fluent Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BaseThread
from ..senders.fluent import FluentSender


class FluentThread(BaseThread):

    def __init__(self, tag="app.debug", host="192.168.11.9", port=24224, **kwargs):
        """

        .. todo:: args

        """
        super(FluentThread, self).__init__(**kwargs)
        self.sender = FluentSender(tag, host=host, port=port)

    def send(self, data):
        """ implements method """
        self.sender.send(data)