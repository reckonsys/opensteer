from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from opensteer.meetings.models import Standup, Checkin


User = get_user_model()
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(
        hour=settings.MEETING_HOUR, minute=settings.MEETING_MINUTE)),
    name="create_meetings",
    ignore_result=True,
)
def create_meetings():
    """Create meetings if required"""
    now = timezone.now()
    day, date, week = now.weekday(), now.date(), int(now.strftime("%U"))
    logger.info('Attempting to create meetings')
    Standup.create_meetings(date=date)
    if day == settings.CHECKIN_DAY:
        Checkin.create_meetings(year=now.year, week=week)
