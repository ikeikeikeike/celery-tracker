from __future__ import print_function
from __future__ import absolute_import


import time
import anyjson
import threading


from . import state


_INTERVAL = 15


class EventStorage(threading.Thread):

    def __init__(self, plugins, interval=_INTERVAL, **kwargs):
        super(EventStorage, self).__init__(**kwargs)

        self.plugins = plugins
        self.interval = interval
        self.state = state
        self.serialize = anyjson
        self.storage = {}
        for plugin_name in self.plugins:
            self.storage.update({plugin_name: []})

    def run(self):
        while True:
            self.set_events()
            time.sleep(self.interval)

    def set_events(self):
        """
        self.state.list_tasks()
        self.state.list_workers()
        self.state.list_task_types()
        self.state.task_state(tasks_id)
        self.state.show_worker(node_name)
        self.state.list_worker_tasks(hostname)
        self.state.list_tasks_by_name(task_name)
        """
        data = []

        for task in self.state.list_task_types():
            data.append({
                "{0}".format(task): self._to_dict(
                    self.state.list_tasks_by_name(task))
            })

        for worker in self.state.list_workers():
            data.append({
                "{0}".format(worker.hostname): self._to_dict(
                    self.state.list_worker_tasks(worker.hostname))
            })

        if data:
            for plugin_name in self.plugins:
                self.storage[plugin_name].append(data)

        # clear events
        self.state.clear()

    def event(self, plugin_name):
        if not self.storage[plugin_name]:
            return []
        return self.storage[plugin_name].pop(0)

    def _to_dict(self, data):
        return self.serialize.deserialize(
            self.serialize.serialize(data))