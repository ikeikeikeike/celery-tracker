# -*- coding: utf-8 -*-
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

    def __init__(self, host, port, metrics, **kwargs):
        """

        .. todo:: verboseの場合 pprint整形、それぞれの送信FLG表示
        """
        super(ZabbixPlugin, self).__init__(**kwargs)

        self.host = host
        self.port = port
        self.metrics = metrics
        self.sender = send_to_zabbix

    def send(self):
        """ implements method """
        metrics = []
        event = self.storage.event("zabbix")

        for event_data in event and event["event"]:
            for name in event_data:
                data = event_data[name]
                for k in data:
                    key = '{0}.{1}.{2}'.format(self.tag, name, k)
                    value = data[k]
                    if self.verbose > 2:
                        self.logger.debug(
                            "ZabbixPlugin: (zabbix-host)%s:%s, (host)%s, (key)%s, (value)%s" % (
                                self.host, self.port, "celery-agent", key, value,
                        ))

                    metrics.append(Metric('celery-agent', key, value))

        if not event:
            self.logger.debug(
                "ZabbixPlugin: (zabbix-host)%s:%s, (tag)%s, (event)%s " % (
                    self.host, self.port, self.tag, event))

        if metrics:
            self.sender(metrics, self.host, self.port)


