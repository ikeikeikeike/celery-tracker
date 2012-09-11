Installation
========================

.. highlight:: bash


*Setup*

::

    $ pip install celery-tracker


celeryconfig and Django settings module.
-------------------------------------------


.. .. note::

..   `CELERY_IGNORE_RESULT`



.. highlight:: python


Create celeryconfig.py, Or edit to settings.py ::

    # Broker - amqp,
    BROKER_URL = "amqp://guest@127.0.0.1//"


    # Path to file storage.  (default: memory),  e.g. /tmp/tracker.db
    CELERY_TRACKER_STORAGE = "/tmp/tracker.db"


    # Log Level
    CELERY_TRACKER_LOG_LEVEL = "INFO"


    # Plugins
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

