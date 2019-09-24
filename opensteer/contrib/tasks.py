from django.contrib.auth import get_user_model

from config import celery_app

User = get_user_model()


@celery_app.task()
def create_meetings():
    """A pointless Celery task to demonstrate usage."""
    u = User.objects.count()
    print(u)
    return u
