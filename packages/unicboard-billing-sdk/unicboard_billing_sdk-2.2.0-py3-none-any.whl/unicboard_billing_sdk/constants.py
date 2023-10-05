from enum import Enum


class ResourceTypeEnum(Enum):
    water = 'water'
    gas = 'gas'
    electricity = 'electricity'
    heat = 'heat'


class IntervalSelectValue(Enum):
    """
    Enumeration of intervals
    """
    half_hour = '30 minute'
    hour = '60 minutes'
    day = '1 day'
    week = '1 week'
    month = '1 month'

    def __repr__(self) -> str:
        return f'{type(self).__name__}.{self.name}'
