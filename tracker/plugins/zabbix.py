"""
Zabbix Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BasePlugin
from zbxsend import (
    send_to_zabbix,
    Metric
)


class ZabbixPlugin(BasePlugin):
    """ Plugin for Zabbix. """

    def __init__(self, host, port, metrics, **kwargs):
        """

        @see celeryconfig.CELERY_TRACKER_PLUGINS

        :param str host: Host name.
        :param int port: Port number.
        :param dict metrics: Metric list.
        """
        super(ZabbixPlugin, self).__init__(**kwargs)

        self.host = host
        self.port = port
        self.metrics = metrics
        self.sender = send_to_zabbix

    def pop_event(self):
        """ Get event tracking data. """
        return self.storage.event("zabbix")

    def running(self):
        """ implements method """
        event = self.pop_event()

        # Used metrics
        metrics = self._average(event)
        if metrics:
            self.sender(metrics, self.host, self.port)
        else:
            self.logger.info("ZabbixPlugin/%s:%s tag: %s event: %r " % (
                self.host, self.port, self.tag, event))

        if self.verbose > 2:
            self._logging(metrics=self._full(event), level="debug")
        else:
            metrics.sort(key=lambda x: (x.host, x.key, x.value, x.clock))
            self._logging(metrics=metrics)

    def _logging(self, metrics, level="info"):
        logger = getattr(self.logger, level)
        if not isinstance(metrics, (tuple, list, set)):
            metrics = [metrics]
        for metric in metrics:
            logger("ZabbixPlugin/%s:%s host: %s key: %s value: %s" % (
                self.host, self.port, metric.host, metric.key, metric.value))

    def _wrap(self, key, value, host="", clock=None):
        return Metric(host=host, key=key, value=value, clock=clock)

    def _add_metrics(self, metrics, key, value, clock=None):
        for dic in self.metrics:
            metrics.append(
                self._wrap(key=key, value=value, host=dic["host"], clock=clock))

    def _average(self, event):
        """ average """
        metrics = []
        average = event and event["workers_average"]
        for key in average:
            self._add_metrics(metrics=metrics, key=key, value=average[key])
        average = event and event["tasks_average"]
        for key in average:
            self._add_metrics(metrics=metrics, key=key, value=average[key])

        return metrics

    def _full(self, event):
        """ verbose """
        metrics = []
        for event_data in event and event["workers"] + event["tasks"]:
            for name in event_data:
                data = event_data[name]
                for k in data:
                    key = '{0}.{1}.{2}'.format(self.tag, name, k)
                    self._add_metrics(metrics=metrics, key=key, value=data[k])

        return metrics
