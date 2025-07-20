import unittest

from scheduler import Scheduler

class TestIsSubset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_is_subset(self):
        self.assertTrue(self.scheduler.is_subset(("10:00", "15:35"), ("10:00", "12:38")))
        self.assertTrue(self.scheduler.is_subset(("11:05", "15:35"), ("11:10", "11:10")))
        self.assertTrue(self.scheduler.is_subset(("10:00", "18:00"), ("10:00", "18:00")))

    def test_is_not_subset(self):
        self.assertFalse(self.scheduler.is_subset(("10:00", "11:30"), ("9:55", "10:30")))
        self.assertFalse(self.scheduler.is_subset(("10:00", "11:30"), ("10:00", "11:31")))
        self.assertFalse(self.scheduler.is_subset(("10:00", "11:30"), ("9:59", "11:31")))
