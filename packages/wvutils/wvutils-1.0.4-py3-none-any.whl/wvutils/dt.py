"""Datetime utilities.

This module contains functions and classes that are used to work with datetimes.
"""

from calendar import monthrange

__all__ = [
    "ALL_DT_FORMATS",
    "dtformats",
    "num_days_in_month",
]


class dtformats:
    """Datetime formats.

    Attributes:
        twitter (str): Twitter datetime format.
        reddit (str): Reddit datetime format.
        general (str): General datetime format.
        db (str): Database datetime format.
        date (str): Date format.
        time_12h (str): 12-hour time format with timezone.
        time_24h (str): 24-hour time format with timezone.
    """

    twitter: str = "%a %b %d %H:%M:%S %z %Y"
    reddit: str = "%b %d %Y %I:%M %p"
    general: str = "%Y-%m-%dT%H:%M:%S%z"
    db: str = "%Y-%m-%d %H:%M:%S"
    date: str = "%Y-%m-%d"
    time_12h: str = "%I:%M %p %Z"
    time_24h: str = "%H:%M %Z"


ALL_DT_FORMATS = [
    dtformats.twitter,
    dtformats.reddit,
    dtformats.general,
    dtformats.db,
    dtformats.date,
    dtformats.time_12h,
    dtformats.time_24h,
]


def num_days_in_month(year: int, month: int) -> int:
    """Determine the number of days in a month.

    Args:
        year (int): Year to check.
        month (int): Month to check.

    Returns:
        int: Number of days in the month.
    """
    return monthrange(year, month)[1]
