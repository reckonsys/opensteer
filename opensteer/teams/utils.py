import pytz
from datetime import datetime

from arrow import Arrow
from dateutil import tz

YEAR = 1882
MONTH = 12
DAY = 11
UTC = 'UTC'
TIMEZONES = [(z, z) for z in pytz.all_timezones]


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
