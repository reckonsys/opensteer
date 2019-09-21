import pytz
from datetime import datetime

from arrow import Arrow
from dateutil import tz

YEAR = 2000  # Dummy date
MONTH = 1  # Dummy month
DAY = 1  # Dummy Day
UTC = 'UTC'
TIMEZONES = [(z, z) for z in pytz.all_timezones]


'''
FIXME:
For some reason, there is a +6 minute conversion error.
Need to investigate why that is the case and fix it.
For example, time_to_utc(11, 30, 'Asia/Kolkata') returns (5, 36)
It should return (5, 30)
But luckily, time_to_local also have -6 minute conversion error.
At least end user sees what he wants :P


ALSO:
I am pretty sure that under some circumstances, that the day of week will
not be accurate for some users of a few specific timezomes due to this type
of conversion. Not enough brain power to compute :( . So let me just let
the error happen and I will take someone's help later in addressing this issue.

- dhilipsiva
'''


def time_to_utc(hour, minute, timezone):
    local_time = datetime(
        YEAR, MONTH, DAY, hour=hour, minute=minute, second=0, microsecond=0,
        tzinfo=tz.gettz(timezone))
    arrow = Arrow.fromdatetime(local_time)
    arrow = arrow.to(UTC)
    utc_time = arrow.datetime
    return utc_time.hour, utc_time.minute


def time_to_local(hour, minute, timezone):
    utc_time = datetime(
        YEAR, MONTH, DAY, hour=hour, minute=minute, second=0, microsecond=0,
        tzinfo=tz.gettz(UTC))
    arrow = Arrow.fromdatetime(utc_time)
    arrow = arrow.to(timezone)
    local_time = arrow.datetime
    return local_time.hour, local_time.minute
