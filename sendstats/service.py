from __future__ import print_function
from __future__ import absolute_import

from celerymon.consumer import EventConsumer
from celerymon.web import WebServerThread


from .utils.loader import import_class
from .configs import settings


class SendStatsService(object):

    def __init__(self, logger, http_port=8989, http_address='', plugins=None):
        """

        .. todo:: Fix plugins settings

        """
        self.logger = logger
        self.http_port = http_port
        self.http_address = http_address
        self.plugins = plugins or []

    def start(self):
        self.plugin_start()
        WebServerThread(port=self.http_port, address=self.http_address).start()
        EventConsumer().start()

    def plugin_start(self):
        for plugin in self.get_plugins():
            plugin().start()

    def get_plugins(self):
        """ From str to class object """
        plugins = settings.CELERY_SENDSTATS_PLUGINS
        if self.plugins:
            plugins = self.plugins
        return [import_class(plugin) for plugin in plugins]


