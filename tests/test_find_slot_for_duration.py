import unittest

from exceptions import InvalidDurationError
from scheduler import Scheduler

class TestFindSlotForDuration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_find_slot_for_duration(self):
        self.assertEqual(self.scheduler.find_slot_for_duration(2, 30), ("2025-02-15", "12:00", "14:30"))
        self.assertEqual(self.scheduler.find_slot_for_duration(8), ("2025-02-19", "09:00", "17:00"))
        self.assertIsInstance(self.scheduler.find_slot_for_duration(10), str)
        self.assertEqual(self.scheduler.find_slot_for_duration(duration_minutes=301), ("2025-02-15", "12:00", "17:01"))


    def test_find_slot_for_duration_invalid_duration(self):
        with self.assertRaises(InvalidDurationError):
            self.scheduler.find_slot_for_duration(24)
            self.scheduler.find_slot_for_duration(23, 60)
            self.scheduler.find_slot_for_duration(duration_minutes=24*60)