"""
This module provides the custom exceptions that may occur in the main file
"""

from typing import List


class InvalidDateFormatError(ValueError):
    def __init__(self, date:str):
        self.date = date

    def __str__(self):
        return f'Invalid date format: {self.date} \n Correct format: YYYY-MM-DD'


class InvalidTimeFormatError(ValueError):
    def __init__(self, time:str):
        self.time = time

    def __str__(self):
        return (f'Invalid time format in {self.time} \n Correct format: HH:MM, '
                f'where HH is the hour and must be in range 0-23,'
                f'MM is the minute and must be in range 0-59')


class KeyDoesNotExistError(KeyError):
    def __init__(self, key:str, existing_keys: List[str]):
        self.key = key
        self.existing_keys = existing_keys
    def __str__(self):
        return f'Key {self.key} does not exist \n Available keys: {self.existing_keys}'


class DataNotFoundError(ValueError):
    def __init__(self, url:str):
        self.url = url

    def __str__(self):
        return f'Data not found at {self.url}'


class InvalidDurationError(ValueError):
    def __init__(self, duration_hours:int, duration_minutes:int):
        self.duration_hours = duration_hours
        self.duration_minutes = duration_minutes
    def __str__(self):
        return (f'Invalid duration {self.duration_hours}:{self.duration_minutes}\n'
                f'The correct duration should be from 0 to 23 hours and from 0 to 59 minutes combined')