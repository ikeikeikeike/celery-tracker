from __future__ import print_function
from __future__ import absolute_import


from celerymon.consumer import EventConsumer
from celerymon.web import WebServerThread


from .utils.loader import import_class


class SendStatsService(object):

    def __init__(self, logger, http_port=12201, http_address='', plugins=None):
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
        """ From str to class object """
        for plugin_name in self.get_plugins():
            plugin = self.plugins[plugin_name]

            klass = import_class(plugin.pop("class"))
            klass(logger=self.logger, **plugin).start()

    def get_plugins(self):
        if isinstance(self.plugins, (tuple, list, set)):
            return [plugin for plugin in plugins if plugin in self.plugins]
        return self.plugins