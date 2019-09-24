import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("opensteer")

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
# every 60 seconds
# print('ASDKJHASLKJDHAKJLSDHKALJSDHLKAJSD')
# sender.add_periodic_task(1.0, 'opensteer.contrib.tasks.create_meetings')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
