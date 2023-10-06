# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from datetime import timedelta


class DateTimeOffset(object):
    """Class representing any time offsets"""

    def __init__(self, days, hours, minutes):
        self.days = days
        self.hours = hours
        self.minutes = minutes

    def __repr__(self):
        return f"DateTimeOffset(Days={self.days},Hours={self.hours},Minutes={self.minutes})"

    def __str__(self):
        return self.__repr__()

    def _to_dict(self):
        return {"days": self.days, "hours": self.hours, "minutes": self.minutes}

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DateTimeOffset):
            return self.days == other.days and self.hours == other.hours and self.minutes == other.minutes
        return False

    def to_timedelta(self):
        return timedelta(days=self.days, hours=self.hours, minutes=self.minutes)
