import unittest

from scheduler import Scheduler


class TestIsAvailable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_is_available(self):
        self.assertTrue(self.scheduler.is_available('2025-02-15', "15:00", "17:30"))
        self.assertTrue(self.scheduler.is_available('2025-02-16', "20:00", "21:11"))
        self.assertTrue(self.scheduler.is_available('2025-02-17', "12:00", "12:30"))

    def test_is_not_available(self):
        self.assertFalse(self.scheduler.is_available('2025-02-15', "17:30", "20:02"))
        self.assertFalse(self.scheduler.is_available('2025-02-16', "22:00", "08:00"))
        self.assertFalse(self.scheduler.is_available('2025-02-17', "12:30", "09:00"))