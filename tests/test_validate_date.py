import unittest

from exceptions import InvalidDateFormatError
from scheduler import Scheduler

class TestValidateDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_valid_date(self):
        self.assertIsNone(self.scheduler.validate_date("2025-02-15"))

    def test_invalid_date(self):
        with self.assertRaises(InvalidDateFormatError):
            self.scheduler.validate_date("20250215")
            self.scheduler.validate_date("02-15-2025")
            self.scheduler.validate_date("15-02-2025")
            self.scheduler.validate_date("2025/02/15")

