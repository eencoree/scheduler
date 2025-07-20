import unittest

from exceptions import InvalidTimeFormatError
from scheduler import Scheduler


class TestIsValidTimeslot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_is_valid_timeslot_strict(self):
        self.assertTrue(self.scheduler.is_valid_timeslot(("10:00", "15:35")))
        self.assertFalse(self.scheduler.is_valid_timeslot(("10:00", "10:00")))

    def test_is_valid_timeslot_subset(self):
        self.assertTrue(self.scheduler.is_valid_timeslot(("10:00", "10:00"), True))

    def test_is_valid_timeslot_invalid(self):
        with self.assertRaises(InvalidTimeFormatError):
            self.scheduler.is_valid_timeslot(("25:00", "10:00"))
            self.scheduler.is_valid_timeslot(("15:00", "10:000"))
            self.scheduler.is_valid_timeslot(("5:00", "10:60"))