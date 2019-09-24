from django.utils import timezone
from django.contrib.auth import get_user_model

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from opensteer.teams.models import Organization


User = get_user_model()
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="create_meetings",
    ignore_result=True
)
def create_meetings():
    """Create meetings if required"""
    now = timezone.now()
    year = now.year
    hour = now.hour
    date = now.date()
    minute = now.minute
    day = now.weekday()
    week = int(now.strftime("%U"))
    for organization in Organization.objects.filter(
            meeting_hour=hour, meeting_minute=minute):
        logger.info(f'Attempting to create meetings for {organization.name}')

        for team in organization.teams.all():
            if team.standups.filter(date=date).count() == 0:
                # We don't have any standups, yet! so lets create one.
                # First, deactivate all old standups
                # TODO: Send emails to Admins & managers stating stale Standups
                # Stale Standups: The ones that are missing responses
                team.standups.filter(is_active=True).update(is_active=False)
                logger.info(f'New Standup for {team.name}')
                standup = team.standups.create(date=date)
                # Send notifications to all members of organization
                logger.info(standup)
            if organization.checkin_day != day:
                # This is not even the day. So don't bother doing anything
                continue
            if team.checkins.filter(year=year, week=week).count() == 0:
                # We don't have any Checkins, yet! so lets create one.
                # First, deactivate all old checkins
                # TODO: Send emails to Admins & managers stating stale Checkins
                # Stale Checkins: The ones that are missing responses
                team.checkins.filter(is_active=True).update(is_active=False)
                logger.info(f'New Checkin for {team.name}')
                checkin = team.checkins.create(year=year, week=week)
                # Send notifications to all members of organization
                logger.info(checkin)
