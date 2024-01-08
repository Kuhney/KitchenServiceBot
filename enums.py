from enum import Enum


class Weekday(Enum):
    MONDAY = (0, "Montag")
    TUESDAY = (1, "Dienstag")
    WEDNESDAY = (2, "Mittwoch")
    THURSDAY = (3, "Donnerstag")
    FRIDAY = (4, "Freitag")
    SATURDAY = (5, "Samstag")
    SUNDAY = (6, "Sonntag")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj
