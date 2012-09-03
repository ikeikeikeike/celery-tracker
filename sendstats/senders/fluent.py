"""
Fluent Sender

"""
from __future__ import print_function
from __future__ import absolute_import


from fluent import sender
from .base import BaseSender


class FluentSender(BaseSender):
    """ Sender class for Fluent. """

    def __init__(self, tag, host, port, **kwargs):
        """

        :param str tag: Tag name
        :param str host: Dest.
        :param int port: port.
        """
        self.sender = sender.FluentSender(tag, host=host, port=port)

    def _send(self, data):
        """ implements method """
        self.sender.emit(None, data)
