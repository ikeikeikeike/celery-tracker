"""
Fluent Plugin

"""
from __future__ import print_function
from __future__ import absolute_import


from .base import BasePlugin
from ..senders.fluent import FluentSender


class FluentPlugin(BasePlugin):

    def __init__(self, **kwargs):
        super(FluentPlugin, self).__init__(**kwargs)

        self.verbose = True
        self.tag  = "app.debug"
        self.host = "192.168.11.9"
        self.port = 24224
        self.sender = FluentSender(
            tag=self.tag, host=self.host, port=self.port)

    def send(self):
        """ implements method """
        self.sender.send(self.send_data())

    def send_data(self):
        data = {
            "state.list_task_types": self.state.list_task_types(),
            "state.list_tasks": self.state.list_tasks(),
            "state.list_workers": self.state.list_workers(),
#            self.state.task_state()
#            self.state.list_tasks_by_name()
#            self.state.list_worker_tasks()
#            self.state.show_worker()
        }

        if self.verbose:
            self.logger.debug(
                "FluentPlugin: (host)%s:%s, (tag)%s, (data)%r " % (
                    self.host, self.port, self.tag, data))

        return data