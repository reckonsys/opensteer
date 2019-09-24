import pytz
from datetime import datetime

from arrow import Arrow
from dateutil import tz

from config.settings.base import TIME_ZONE
from opensteer.teams.choices import DayOfWeek

YEAR = 2000  # Dummy date
MONTH = 1  # Dummy month
DAY = 1  # Dummy Day
TIMEZONES = [(z, z) for z in pytz.all_timezones]


'''
FIXME:  [random confusion]
For some reason, there is a +6 minute conversion error.
Need to investigate why that is the case and fix it.
For example, time_to_utc(11, 30, 'Asia/Kolkata') returns (5, 36)
It should return (5, 30)
But luckily, time_to_local also have -6 minute conversion error.
At least end user sees what he wants :P
'''


def to_server_tz(hour, minute, timezone, day=None):
    local_time = datetime(
        YEAR, MONTH, DAY, hour=hour, minute=minute, second=0, microsecond=0,
        tzinfo=tz.gettz(timezone))
    arrow = Arrow.fromdatetime(local_time)
    arrow = arrow.to(TIME_ZONE)
    utc_time = arrow.datetime
    if local_time.day > utc_time.day:
        day = DayOfWeek.next(day)
    elif local_time.day < utc_time.day:
        day = DayOfWeek.previous(day)
    return utc_time.hour, utc_time.minute, day


def to_org_tz(hour, minute, timezone, day=None):
    utc_time = datetime(
        YEAR, MONTH, DAY, hour=hour, minute=minute, second=0, microsecond=0,
        tzinfo=tz.gettz(TIME_ZONE))
    arrow = Arrow.fromdatetime(utc_time)
    arrow = arrow.to(timezone)
    local_time = arrow.datetime
    if utc_time.day < local_time.day:
        day = DayOfWeek.next(day)
    elif utc_time.day > local_time.day:
        day = DayOfWeek.previous(day)
    return local_time.hour, local_time.minute, day
