from __future__ import division
from __future__ import print_function
from __future__ import absolute_import


import time
import shelve
import anyjson
import threading
import itertools


from . import state


_INTERVAL = 15


class EventStorage(threading.Thread):

    def __init__(self, plugins, storage, interval=_INTERVAL, **kwargs):
        """
        Event Storage class.

        :param list plugins: Plugin list.
        :param str storage: Path to storage.
        :param int interval: Interval in seconds.
        """
        super(EventStorage, self).__init__(**kwargs)

        self.state = state
        self.plugins = plugins
        self.interval = interval
        self.serialize = anyjson
        self.cv = threading.Condition()
        self.storage = storage and \
                       shelve.open(storage, protocol=2, writeback=True)
        for plugin_name in self.plugins:
            if plugin_name not in self.storage:
                self.storage.update({plugin_name: {}})

    def run(self):
        """
        Runner
        """
        while True:
            self.set_events()
            time.sleep(self.interval)

    def set_events(self):
        """ Set event tracking data. """
        tasks = []
        workers = []

        for task in self.state.list_task_types():
            for task_data in self.state.list_tasks_by_name(task):
                tasks.append({
                    "{0}".format(task): self._to_dict(task_data[1])
                })

        for worker in self.state.list_workers():
            for worker_data in self.state.list_worker_tasks(worker.hostname):
                workers.append({
                    "{0}".format(worker.hostname): self._to_dict(worker_data[1])
                })

        # set event to storage
        self._set_storage(tasks=tasks, workers=workers)

        # clear events
        self.state.clear()

    def event(self, plugin_name):
        """
        Get event tracking data.

        .. todo:: Wrapped return object. Add Interface method.

        :param str plugin_name: Select from a plugins package.
        :rtype: dict
        :return: event tracking data.
        """
        with self.cv:
            while not self.storage[plugin_name]:
                self.cv.wait()
            event = self.storage[plugin_name].copy()
            self._clear_storage(plugin_name)
            return event

    def _set_storage(self, tasks, workers):
        with self.cv:
            for plugin_name in self.plugins:
                events = self.storage[plugin_name]
                # set events
                self.storage[plugin_name].update(
                    self._merge_events(events=events, tasks=tasks, workers=workers))
            # sync
            self._sync_storage()

            # unlock
            self.cv.notifyAll()

    def _sync_storage(self):
        """ for the file storage """
        try:
            self.storage.sync()
        except Exception:
            pass

    def _clear_storage(self, plugin_name):
        try:
            self.storage[plugin_name].clear()
        except Exception:
            pass

    def _merge_events(self, events, tasks, workers):
#        tasks_original = self.state.tasks()
#        workers_original = self.state.workers()
        tasks_ = events.get("tasks", [])
        workers_ = events.get("workers", [])
        tasks_.extend(tasks)
        workers_.extend(workers)
        return {
            "tasks": tasks_,
            "workers": workers_,
            "tasks_average": self._to_average(tasks_),
            "workers_average": self._to_average(workers_)
        }

    def _to_average(self, events):
        avg = {}
        for key, groups in itertools.groupby(events, lambda dic: dic.keys()[0]):
            number, retry, runtime = 0, 0, []
            for group in groups:
                g = group[key]
                number += 1
                retry += g["retries"] or 0
                runtime.append(g["runtime"])
            runtimes = [r for r in runtime if r]

            try:
                avg.update({
                    "runtime_{0}".format(key): sum(runtimes) / len(runtimes)})
            except ZeroDivisionError:
                avg.update({"runtime_{0}".format(key): 0})
            avg.update({"number_of_{0}".format(key): number})
            avg.update({"retry_sum_{0}".format(key): retry})

        return avg

    def _to_dict(self, data):
        return self.serialize.deserialize(self.serialize.serialize(data))
