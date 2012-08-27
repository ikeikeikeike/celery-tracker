"""
Logging Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BasePlugin


class LoggingPlugin(BasePlugin):

    def send(self):
        """ implements method """
        print("send logging")