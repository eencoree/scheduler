import unittest

from exceptions import KeyDoesNotExistError
from scheduler import Scheduler


class TestGetDayFromDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_correct_date(self):
        day = self.scheduler.get_day_from_date('2025-02-15')
        self.assertIsNotNone(day)
        self.assertIsInstance(day, dict)
        self.assertEqual(day['date'], '2025-02-15')

    def test_not_exist_date(self):
        with self.assertRaises(KeyDoesNotExistError):
            self.scheduler.get_day_from_date('2030-02-15')
            self.scheduler.get_day_from_date('2030-02-15')
            self.scheduler.get_day_from_date('2030-02-15')

