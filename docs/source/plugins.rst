Plugins
==========

Booting plugins

* Zabbix - zabbix post threading.Thread
* Fluent - Flutnd post threading.Thread
* Nagios - Nagios post threading.Thread
* Munin  - Munin  post threading.Thread

Set arguments
-----------------------

.. highlight:: bash


::

    $ celry sendstas --plugins=zabbix,nagios,munin,fluent


Configuration file
--------------------

.. highlight:: python


::

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
        #"logging": {
        #    "class": "sendstats.plugins.logging.LoggingPlugin",
        #    "tag": "celery.sendstats",
        #    "interval": 10,
        #    "verbose": True
        #},
    }


Reference
--------------------


Base
~~~~~~~~~~

.. autoclass:: sendstats.plugins.base.BasePlugin
   :members:

Zabbix
~~~~~~~

.. autoclass:: sendstats.plugins.zabbix.ZabbixPlugin
   :members:

Fluent
~~~~~~~~~~

.. autoclass:: sendstats.plugins.fluent.FluentPlugin
   :members:


