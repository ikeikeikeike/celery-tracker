"""
Fluent Sender

"""
from __future__ import print_function
from __future__ import absolute_import


from fluent import sender
from .base import BaseSender


class FluentSender(BaseSender):

    def __init__(self, tag="app.debug", host="192.168.11.9", port=24224, **kwargs):
        """

        .. todo:: args

        """
        self.sender = sender.FluentSender(tag, host=host, port=port)

    def send(self, data):
        """ implements method """
        self.sender.emit(None, data)
