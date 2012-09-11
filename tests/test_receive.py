import logging

from tracker.configs.celeryconfig import CELERY_TRACKER_PLUGINS
from tracker.plugins.receive import ReceivePlugin

try:
    from .utils import MockStorage
except (ImportError, ValueError):
    from tests.utils import MockStorage


config = CELERY_TRACKER_PLUGINS["receive"]


def get_kwargs():
    return {
        "logger": logging.getLogger("test_receive"),
        "tag": config["tag"],
        "storage": MockStorage(),
        "host": config["host"],
        "port": config["port"]
    }


def test_event():
    plugin = ReceivePlugin(**get_kwargs())
    assert isinstance(plugin.pop_event(), (dict, ))


#def test_average():
#    plugin = ReceivePlugin(**get_kwargs())
#    average = plugin._average(plugin.pop_event())
#    assert isinstance(average, (list, ))
#    assert len(average) == 6
#    for obj in average:
#        assert isinstance(obj, (Metric, ))


#def test_send():
#    def assert_sender(metrics, host, port):
#        assert isinstance(metrics, (list, tuple, set))
#        assert isinstance(host, (str, ))
#        assert isinstance(port, (int, ))
#        for obj in metrics:
#            assert isinstance(obj, (Metric, ))
#
#    plugin = ReceivePlugin(**get_kwargs())
#    plugin.sender = assert_sender
#    plugin.running()


#def test_logging():
#    plugin = ReceivePlugin(**get_kwargs())
#    metrics = [Metric("host-{0}".format(i), "key-{0}".format(i), "value-{0}".format(i))
#                for i in range(0, 10)]
#    plugin._logging(metrics[0], "info")
#    plugin._logging(metrics, "info")
#    plugin._logging(metrics, "warning")
#    plugin._logging(metrics, "critical")
#    plugin._logging(metrics, "debug")
