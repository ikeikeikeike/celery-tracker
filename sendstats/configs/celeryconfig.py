"""
Global Settings

"""
try:
    settings = __import__("django.conf.settings")
except ImportError, e:
    settings = {}


# Broker - amqp,
BROKER_URL = getattr(settings, "BROKER_URL", "amqp://guest@127.0.0.1//")


# file storage path (default: memory)
#CELERY_SENDSTATS_STORAGE = "/tmp/sendstats.db"


# Log Level
CELERY_SENDSTATS_LOG_LEVEL = getattr(settings, "CELERY_SENDSTATS_LOG_LEVEL", "DEBUG")


# plugins
CELERY_SENDSTATS_PLUGINS = getattr(settings, "CELERY_SENDSTATS_PLUGINS", {
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
})
