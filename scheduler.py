"""
This module provides a class for processing an employee's schedule
"""

import datetime
from itertools import repeat
from typing import Dict, List, Tuple, Union

import requests
from exceptions import (
    InvalidDateFormatError,
    KeyDoesNotExistError,
    InvalidTimeFormatError,
    DataNotFoundError,
    InvalidDurationError,
)

Timeslot = Tuple[str, str]
Slot = List[Timeslot]
MyDict = Dict[str, Slot]


class Scheduler:
    """
    Class for processing an employee's schedule
    """

    def __init__(self, url: str):
        """
        Checks the response by url and stores the data in the data variable,
        also creates dictionaries for quick access to busy and free time intervals.
        :param url: the url for accessing the data
        """
        self.response = requests.get(url)
        self.free_slots: MyDict = {}
        self.busy_slots: MyDict = {}
        if self.response.status_code == requests.codes.ok:
            self.data = self.response.json()
        else:
            raise DataNotFoundError(url)

    @staticmethod
    def validate_date(date: str) -> None:
        """
        Checks that the given date is in the valid format
        :param date: the date to check
        :return: None or raise an exception
        """
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            raise InvalidDateFormatError(date) from e

    @staticmethod
    def is_valid_timeslot(timeslot: Timeslot, allow_zero: bool = False) -> bool:
        """
        Checks that the given timeslot is free
        :param timeslot: the timeslot to check
        :param allow_zero: a parameter for checking whether one time interval is a subset of another
        :return: True if the timeslot is free, False otherwise
        """
        try:
            start = datetime.datetime.strptime(timeslot[0], "%H:%M")
            end = datetime.datetime.strptime(timeslot[1], "%H:%M")
            timedelta = end - start
        except ValueError as e:
            raise InvalidTimeFormatError(timeslot) from e
        return (
            timedelta.total_seconds() >= 0
            if allow_zero
            else timedelta.total_seconds() > 0
        )

    def is_subset(self, free_time_range: Timeslot, sub_time_range: Timeslot) -> bool:
        """
        Checks whether a given time interval is a subset of a free time interval
        :param free_time_range: the free time interval
        :param sub_time_range: the time interval for checking the subset
        :return: True if the given time interval is a subset of a free time interval, False otherwise
        """
        return (
                self.is_valid_timeslot(sub_time_range, True)
                and self.is_valid_timeslot((free_time_range[0], sub_time_range[0]), True)
                and self.is_valid_timeslot((sub_time_range[1], free_time_range[1]), True)
                and self.is_valid_timeslot((free_time_range[0], sub_time_range[1]), True)
                and self.is_valid_timeslot((sub_time_range[0], free_time_range[1]), True)
        )

    def get_day_from_date(self, date: str) -> Dict:
        """
        Gets a day dictionary containing information about it
        :param date: the date for receiving information about the day
        :return: day dictionary
        """
        self.validate_date(date)
        day_from_date = tuple(
            filter(lambda day: day["date"] == date, self.data["days"])
        )
        if not day_from_date:
            raise KeyDoesNotExistError(date, [d["date"] for d in self.data["days"]])
        return day_from_date[0]

    def get_busy_slots(self, date: str) -> Slot:
        """
        Collects all occupied time intervals on a specific date
        :param date: the date for receiving information about the day
        :return: the list of busy time intervals
        """
        day = self.get_day_from_date(date)
        day_timeslots = tuple(
            filter(
                lambda timeslot: timeslot["day_id"] == day["id"], self.data["timeslots"]
            )
        )
        if not self.busy_slots.get(date):
            self.busy_slots[date] = sorted(
                set(
                    (day_timeslot["start"], day_timeslot["end"])
                    for day_timeslot in day_timeslots
                )
            )

        return self.busy_slots[date]

    def get_free_slots(self, date: str) -> Slot:
        """
        Collects all free time intervals on a specific date
        :param date: the date for receiving information about the day
        :return: the list of free time intervals
        """
        day = self.get_day_from_date(date)

        if self.free_slots.get(date):
            return self.free_slots.get(date)

        self.free_slots[date] = [(day["start"], day["end"])]

        if self.busy_slots.get(date):
            busy_slots = self.busy_slots.get(date)
        else:
            busy_slots = self.get_busy_slots(date)

        if busy_slots:
            potential_free_slots = [
                (day["start"], busy_slots[0][0]),
                (busy_slots[-1][1], day["end"]),
            ]

            for i in range(len(busy_slots) - 1):
                potential_free_slots.append((busy_slots[i][1], busy_slots[i + 1][0]))

            self.free_slots[date] = sorted(
                filter(self.is_valid_timeslot, potential_free_slots)
            )
        return self.free_slots[date]

    def is_available(self, date: str, time_start: str, time_end: str) -> bool:
        """
        Checks whether a given time interval is available for a given date
        :param date: the date to check
        :param time_start: the start time of the time interval
        :param time_end: the end time of the time interval
        :return: True if the given time interval is available, False otherwise
        """
        if not self.is_valid_timeslot((time_start, time_end)):
            return False

        if self.free_slots.get(date):
            free_slots = self.free_slots.get(date)
        else:
            free_slots = self.get_free_slots(date)
        return any(map(self.is_subset, free_slots, repeat((time_start, time_end))))

    def find_slot_for_duration(
            self, duration_hours: int = 0, duration_minutes: int = 0
    ) -> Union[Tuple[str, str, str], str]:
        """
        Finds the first free time interval corresponding to the specified time duration
        :param duration_hours: hours of duration
        :param duration_minutes: minutes of duration
        :return: the free time interval corresponding to the specified time duration
        """
        time_duration = datetime.timedelta(
            hours=duration_hours, minutes=duration_minutes
        )
        if time_duration.days == 0:
            for day in self.data["days"]:
                date = day["date"]
                if self.free_slots.get(date):
                    free_slots = self.free_slots.get(date)
                else:
                    free_slots = self.get_free_slots(date)

                for free_slot in free_slots:
                    try:
                        start_time = datetime.datetime.strptime(free_slot[0], "%H:%M")
                    except ValueError as e:
                        raise InvalidTimeFormatError(free_slot[0]) from e

                    duration_time_end = start_time + time_duration
                    start_time = start_time.time().isoformat(timespec="minutes")
                    end_time = duration_time_end.time().isoformat(timespec="minutes")
                    if self.is_subset(free_slot, (start_time, end_time)):
                        return date, free_slot[0], end_time
        else:
            raise InvalidDurationError(duration_hours, duration_minutes)
        return "There is no free time in the schedule for the specified duration of the application"
