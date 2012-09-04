Customize
===========


Customize plugin
------------------------

Inherit BasePlugin, Define a MyPlugin class.

::

    """
    Customize Plugin

    """
    from sendstats.plugins.base import BasePlugin
    import MySender

    class MyPlugin(BasePlugin):
        """ Plugin for Mine. """

        def __init__(self, host, port, **kwargs):
            super(MyPlugin, self).__init__(**kwargs)

            self.host = host
            self.port = port
            self.sender = MySender(
                tag=self.tag, host=self.host, port=self.port)

        def send(self):
            """ implements method """
            event = self.storage.event("my")  #  CELERY_SENDSTATS_PLUGINS key.

            workers_average = event and event["workers_average"]
            self.sender.send(workers_average)

            tasks_average = event and event["tasks_average"]
            self.sender.send(tasks_average)

            self._logging(workers_average)
            self._logging(tasks_average)
            if self.verbose > 0:
                self._logging(event, "debug")

        def _logging(self, event, level="info"):
            logger = getattr(self.logger, level)
            logger("MyPlugin/%s:%s tag: %s event: %r " % (
                self.host, self.port, self.tag, event))


.. highlight:: ruby

And set the MyPlugin into configuration file. [ @celeryconfig.py, @settings.py ]

::

    # plugins
    CELERY_SENDSTATS_PLUGINS = {
        "fluent": {
            "class": "sendstats.plugins.fluent.FluentPlugin",
            "verbose": 0,
            "interval": 20,
            "tag": "celery.sendstats",
            "host": "127.0.0.1",
            "port": 24224
        },
        "zabbix": {
            "class": "sendstats.plugins.zabbix.ZabbixPlugin",
            "verbose": 0,
            "interval": 20,
            "tag": "celery.sendstats",
            "host": "127.0.0.1",
            "port": 10051,
            "metrics": [
                {"host": "celery-agent"},
            ]
        },
        "my": {
            "class": "path.to.MyPlugin",
            "verbose": 0
            "interval": 15,
            "tag": "celery.sendstats",
            "host": "127.0.0.1",
            "port": 10101,
        },
    }

