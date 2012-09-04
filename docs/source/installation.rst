Installation
========================

.. highlight:: bash


*Setup*

::

    $ pip install celery-sendstats


celeryconfig and Django settings module.
-------------------------------------------


.. .. note::

..   `CELERY_IGNORE_RESULT`



.. highlight:: python


Create celeryconfig.py, Or edit to settings.py ::

    # Broker - amqp,
    BROKER_URL = "amqp://guest@127.0.0.1//"


    # Path to file storage.  (default: memory),  e.g. /tmp/sendstats.db
    CELERY_SENDSTATS_STORAGE = "/tmp/sendstats.db"


    # Log Level
    CELERY_SENDSTATS_LOG_LEVEL = "INFO"


    # Plugins
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



