import unittest

from scheduler import Scheduler

class TestGetFreeSlots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(url="https://ofc-test-01.tspb.su/test-task/")

    def test_free_slots(self):
        free_slots_date_1 = [("12:00", "17:30"), ("20:00", "21:00")]
        free_slots_date_2 = [("08:00", "09:30"), ("11:00", "14:30"), ("18:00", "22:00")]
        free_slots_date_3 = [("09:00", "12:30")]
        free_slots_date_4 = [("11:00", "11:30"), ("16:00", "17:00")]
        free_slots_date_5 = [("09:00", "18:00")]

        free_slots_iterator = iter(
            [
            free_slots_date_1, free_slots_date_2, free_slots_date_3,
                                    free_slots_date_4, free_slots_date_5
            ]
        )

        for i, day in enumerate(self.scheduler.data['days']):
            self.assertEqual(next(free_slots_iterator), self.scheduler.get_free_slots(day['date']))