"""
Global Settings

"""
settings = {}
# try:
    # conf = __import__("django.conf")
    # settings = conf.conf.settings
# except ImportError:
    # settings = {}


# Broker - amqp,
BROKER_URL = getattr(settings, "BROKER_URL", "amqp://guest@127.0.0.1//")


# file storage path (default: memory),  e.g. /tmp/tracker.db
CELERY_TRACKER_STORAGE = getattr(settings, "CELERY_TRACKER_STORAGE", "")


# Log level
CELERY_TRACKER_LOG_LEVEL = getattr(settings, "CELERY_TRACKER_LOG_LEVEL", "INFO")


# plugins
CELERY_TRACKER_PLUGINS = getattr(settings, "CELERY_TRACKER_PLUGINS", {
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
})
