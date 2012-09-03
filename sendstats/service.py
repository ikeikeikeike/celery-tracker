from __future__ import print_function
from __future__ import absolute_import


from celerymon.consumer import EventConsumer
from celerymon.web import WebServerThread


from .utils.loader import import_class
from .tracking.storage import EventStorage


class SendStatsService(object):

    def __init__(self, logger, http_port=12201, http_address='',
                 plugins=None, storage=None, **kwargs):
        self.logger = logger
        self.http_port = http_port
        self.http_address = http_address
        self.plugins = plugins or []
        self.storage = storage or {}

    def start(self):
        WebServerThread(port=self.http_port, address=self.http_address).start()
        storage = EventStorage(plugins=self.get_plugins(), storage=self.storage)
        self.plugin_start(storage)
        storage.start()
        EventConsumer().start()

    def plugin_start(self, storage):
        """ From str to class object """
        for plugin_name in self.get_plugins():
            plugin = self.plugins[plugin_name]

            klass = import_class(plugin.pop("class"))
            klass(logger=self.logger, storage=storage, **plugin).start()

    def get_plugins(self):
        if isinstance(self.plugins, (tuple, list, set)):
            return [p for p in plugins if p in self.plugins]
        return self.plugins