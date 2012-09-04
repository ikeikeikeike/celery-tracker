import logging

from zbxsend import Metric
from sendstats.configs.celeryconfig import CELERY_SENDSTATS_PLUGINS
from sendstats.plugins.zabbix import ZabbixPlugin


config = CELERY_SENDSTATS_PLUGINS["zabbix"]


class MockStorage(object):

    def event(self, plugin_name):
        return {
            "tasks": [],
            "workers": [],
            "tasks_average": {
               "test1": 1,
               "test2": 2,
               "test3": 3,
            },
            "workers_average": {
               "test1": 1,
               "test2": 2,
               "test3": 3,
            }
        }


def get_kwargs():
    return {
        "logger": logging.getLogger("test_zabbix"),
        "tag": config["tag"],
        "storage": MockStorage(),
        "host": config["host"],
        "port": config["port"],
        "metrics": config["metrics"],
    }


def test_event():
    plugin = ZabbixPlugin(**get_kwargs())
    assert isinstance(plugin.pop_event(), (dict, ))


def test_average():
    plugin = ZabbixPlugin(**get_kwargs())
    average = plugin._average(plugin.pop_event())
    assert isinstance(average, (list, ))
    assert len(average) == 6
    for obj in average:
        assert isinstance(obj, (Metric, ))


def test_send():
    plugin = ZabbixPlugin(**get_kwargs())
    plugin.send()


def test_logging():
    plugin = ZabbixPlugin(**get_kwargs())
    metrics = [Metric("host-{0}".format(i), "key-{0}".format(i), "value-{0}".format(i))
                for i in range(0, 10)]
    plugin._logging(metrics[0], "info")
    plugin._logging(metrics, "info")
    plugin._logging(metrics, "warning")
    plugin._logging(metrics, "critical")
    plugin._logging(metrics, "debug")
