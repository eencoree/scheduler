import unittest

from scheduler import Scheduler

class TestGetBusySlots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_get_busy_slots(self):
        actual_busy_slots = [("09:00", "12:00"), ("17:30", "20:00")]
        self.assertEqual(self.scheduler.get_busy_slots('2025-02-15'), actual_busy_slots)
        self.assertEqual(self.scheduler.get_busy_slots('2025-02-19'), [])
