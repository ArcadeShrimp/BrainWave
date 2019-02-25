from unittest import TestCase
from command import Tracker, DataRecord


class TestTracker(TestCase):
    def test_get_threshold(self):
        t = Tracker(None, None)
        t.data_records = {
            ('relax', 0): "Data1",
            ('relax', 1): "Data2",
            ('focus', 2): "Data3"
        }
        t.get_threshold()

