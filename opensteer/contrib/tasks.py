from django.utils import timezone
from django.contrib.auth import get_user_model

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from opensteer.teams.models import Organization


User = get_user_model()
logger = get_task_logger(__name__)


def _create_standup(team, date):
    if not team.standups.filter(date=date).exists():
        return
    # We don't have any standups, yet! so lets create one.
    # First, deactivate all old standups
    # TODO: Send emails to Admins & managers stating stale Standups
    # Stale Standups: The ones that are missing responses
    team.standups.filter(is_active=True).update(is_active=False)
    logger.info(f'New Standup for {team.name}')
    standup = team.standups.create(date=date)
    # Send notifications to all members of organization
    logger.info(standup)
    return standup


def _create_checkin(team, year, week):
    if not team.checkins.filter(year=year, week=week).exists():
        return
    # We don't have any Checkins, yet! so lets create one.
    # First, deactivate all old checkins
    # TODO: Send emails to Admins & managers stating stale Checkins
    # Stale Checkins: The ones that are missing responses
    team.checkins.filter(is_active=True).update(is_active=False)
    logger.info(f'New Checkin for {team.name}')
    checkin = team.checkins.create(year=year, week=week)
    # Send notifications to all members of organization
    logger.info(checkin)
    return checkin


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="create_meetings",
    ignore_result=True
)
def create_meetings():
    """Create meetings if required"""
    now = timezone.now()
    year, hour, minute = now.year, now.hour, now.minute
    day, date, week = now.weekday(), now.date(), int(now.strftime("%U"))
    for organization in Organization.objects.filter(
            meeting_hour=hour, meeting_minute=minute):
        logger.info(f'Attempting to create meetings for {organization.name}')
        for team in organization.teams.all():
            _create_standup(team, date)
            if organization.checkin_day == day:
                _create_checkin(team, year, week)
