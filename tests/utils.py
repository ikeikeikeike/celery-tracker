"""

Utils for unittest
"""


class MockStorage(object):

    def event(self, *args, **kwargs):
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
