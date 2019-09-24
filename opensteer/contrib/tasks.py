from django.contrib.auth import get_user_model
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

# from config import celery_app

User = get_user_model()
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="create_meetings",
    ignore_result=True
)
def create_meetings():
    # @celery_app.task()
    """A pointless Celery task to demonstrate usage."""
    u = User.objects.count()
    logger.info(u)
    print(u)
    return u


rom django.utils import timezone

now = timezone.now()
