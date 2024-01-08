from enum import Enum


class Weekday(Enum):
    MONDAY = (0, "Montag", "mon")
    TUESDAY = (1, "Dienstag", "tue")
    WEDNESDAY = (2, "Mittwoch", "wed")
    THURSDAY = (3, "Donnerstag", "thu")
    FRIDAY = (4, "Freitag", "fri")
    SATURDAY = (5, "Samstag", "sat")
    SUNDAY = (6, "Sonntag", "sun")

    def __new__(cls, value: int, display_name: str, cron: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        obj.cron = cron
        return obj
