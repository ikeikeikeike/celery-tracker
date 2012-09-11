Plugins
==========

Booting plugins

* Zabbix  - Zabbix  threading.Thread
* Fluent  - Flutnd  threading.Thread
* Receive - Receive threading.Thread


Configuration file
--------------------

.. highlight:: python


::

    CELERY_TRACKER_PLUGINS = {
        "fluent": {
            "class": "tracker.plugins.fluent.FluentPlugin",
            "verbose": 0,
            "interval": 20,
            "tag": "celery.tracker",
            "host": "127.0.0.1",
            "port": 24224
        },
        "zabbix": {
            "class": "tracker.plugins.zabbix.ZabbixPlugin",
            "verbose": 0,
            "interval": 20,
            "tag": "celery.tracker",
            "host": "127.0.0.1",
            "port": 10051,
            "metrics": [
                {"host": "celery-agent"},
            ]
        },
        "receive": {
            "class": "tracker.plugins.receive.ReceivePlugin",
            "verbose": 0,
            "tag": "celery.tracker",
            "host": "0.0.0.0",
            "port": 27015,
        },
        #"logging": {
        #    "class": "tracker.plugins.logging.LoggingPlugin",
        #    "tag": "celery.tracker",
        #    "interval": 10,
        #    "verbose": True
        #},
    }


Reference
--------------------


Base
~~~~~~~~~~


.. automodule:: tracker.plugins.base
   :members:
   :undoc-members:

Zabbix
~~~~~~~

.. automodule:: tracker.plugins.zabbix
   :members:
   :undoc-members:

Fluent
~~~~~~~~~~

.. automodule:: tracker.plugins.fluent
   :members:
   :undoc-members:

Receive
~~~~~~~~~~

.. automodule:: tracker.plugins.receive
   :members:
   :undoc-members:


