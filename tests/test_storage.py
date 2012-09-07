from tracker.configs.celeryconfig import CELERY_TRACKER_PLUGINS
from tracker.tracking.storage import EventStorage

try:
    from .utils import MockStorage
except (ImportError, ValueError):
    from tests.utils import MockStorage


def get_events():
    dic = {"retries": 4 , "runtime": 0.21212, "worker": 8}
    return [{"retries": dic , "runtime": dic, "worker": dic} for i in range(0, 10)]


def test_dict():
    storage = EventStorage(plugins=CELERY_TRACKER_PLUGINS, storage={})
    dic = storage._to_dict(dict(a=1, b=2, c=3, d=4, e=5))
    assert(isinstance(dic, (dict, )))


def test_average():
    storage = EventStorage(plugins=CELERY_TRACKER_PLUGINS, storage={})
    average = storage._to_average(get_events())
    assert average["number_of_retries"] == 10
    assert average["retry_sum_retries"] == 40
    assert average["runtime_retries"] == 0.21212000000000003


def test_merge():
    mock_storage = MockStorage()
    storage = EventStorage(plugins=CELERY_TRACKER_PLUGINS, storage={})
    event1 = mock_storage.event()
    event2 = storage._merge_events(event1, get_events(), get_events())
    for k1, k2 in zip(event1, event2):
        data1, data2 = event1[k1], event2[k2]
        assert k1 == k2
        assert type(data1) == type(data2)
