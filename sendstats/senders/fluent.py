"""
Fluent Sender

"""
from __future__ import print_function
from __future__ import absolute_import


from fluent import sender
from .base import BaseSender


class FluentSender(BaseSender):

    def __init__(self, tag, host, port, **kwargs):
        self.sender = sender.FluentSender(tag, host=host, port=port)
        self.verbose = True

    def _send(self, data):
        """ implements method """
        self.sender.emit(None, data)
