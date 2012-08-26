"""
Global Settings

"""
try:
    settings = __import__("django.conf.settings")
except ImportError, e:
    settings = {}


CELERY_SENDSTATS_PLUGINS = getattr(settings, "CELERY_SENDSTATS_PLUGINS", tuple())