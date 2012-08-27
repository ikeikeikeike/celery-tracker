"""
Fluent Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


import anyjson


from .base import BasePlugin
from ..senders.fluent import FluentSender


class FluentPlugin(BasePlugin):

    def __init__(self, tag, host, port, **kwargs):
        super(FluentPlugin, self).__init__(**kwargs)

        self.tag  = tag
        self.host = host
        self.port = port
        self.sender = FluentSender(
            tag=self.tag, host=self.host, port=self.port)

    def send(self):
        """ implements method """
        for data in self.send_data():
            if self.verbose:
                self.logger.debug(
                    "FluentPlugin: (host)%s:%s, (tag)%s, (data)%r " % (
                        self.host, self.port, self.tag, data))
            self.sender.send(data)

    def _to_dict(self, data):
        return anyjson.deserialize(anyjson.serialize(data))

    def send_data(self):
        """
        self.state.list_task_types()
        self.state.list_tasks()
        self.state.list_workers()
        self.state.task_state(tasks_id)
        self.state.list_tasks_by_name(task_name)
        self.state.list_worker_tasks(hostname)
        self.state.show_worker": self.state.show_worker(node_name)
        """
        data = []

        for task in self.state.list_task_types():
            data.append({
                "{0}.{1}".format(self.tag, task): self._to_dict(
                    self.state.list_tasks_by_name(task))
            })

        for worker in self.state.list_workers():
            hostname = worker.hostname
            data.append({
                "{0}.{1}".format(self.tag, hostname): self._to_dict(
                    self.state.list_worker_tasks(hostname))
            })

        return data