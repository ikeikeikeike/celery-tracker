"""
Logging Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BaseThread


class LoggingThread(BaseThread):

    def send(self):
        """ implements method """
        print("send logging")