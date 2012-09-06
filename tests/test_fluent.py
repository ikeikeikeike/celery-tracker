import logging

from sendstats.configs.celeryconfig import CELERY_SENDSTATS_PLUGINS
from sendstats.plugins.fluent import FluentPlugin

try:
    from .utils import MockStorage
except (ImportError, ValueError):
    from tests.utils import MockStorage


config = CELERY_SENDSTATS_PLUGINS["fluent"]


def get_kwargs():
    return {
        "logger": logging.getLogger("test_fluent"),
        "tag": config["tag"],
        "storage": MockStorage(),
        "host": config["host"],
        "port": config["port"],
    }


def test_event():
    plugin = FluentPlugin(**get_kwargs())
    assert isinstance(plugin.pop_event(), (dict, ))


def test_send():
    def assert_sender(x):
        assert isinstance(x, (dict, ))

    plugin = FluentPlugin(**get_kwargs())
    plugin.sender.send = assert_sender
    plugin.send()
