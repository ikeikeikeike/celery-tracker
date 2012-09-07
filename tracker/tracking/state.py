from __future__ import print_function
from __future__ import absolute_import


from celery import states
from celery.events.state import state


def task_state(task_id):
    try:
        task = state.tasks[task_id.strip('/')]
    except KeyError:
        raise KeyError("Unknown task: {0}".format(task_id))
    if task.state in states.EXCEPTION_STATES:
        return task.info(extra=["traceback"])
    return task.info()


def list_tasks(limit=None):
    limit = limit and int(limit) or None
    return state.tasks_by_timestamp(limit=limit)


def list_tasks_by_name(name, limit=None):
    limit = limit and int(limit) or None
    return state.tasks_by_type(name, limit=limit)


def list_task_types():
    return state.task_types()


def list_workers():
    return state.alive_workers()


def show_worker(node_name):
    try:
        return state.workers[node_name]
    except KeyError:
        raise KeyError(
            "Unknown worker node: {0}".format(node_name))


def clear():
    state.clear()


def tasks():
    return state.tasks


def workers():
    return state.workers


def list_worker_tasks(hostname, limit=None):
    limit = limit and int(limit) or None
    return state.tasks_by_worker(hostname, limit=limit)
