# -*- coding: utf-8 -*-

# Broker - amqp,
BROKER_URL = "amqp://guest@192.168.57.134//"

# Debug
#CELERY_SENDSTATS_LOG_LEVEL = True

# Log Level
CELERY_SENDSTATS_LOG_LEVEL = "DEBUG"

# plugins
CELERY_SENDSTATS_PLUGINS = (
    "sendstats.plugins.fluent.FluentThread",
    "sendstats.plugins.logging.LoggingThread",
)