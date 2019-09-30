from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    name = 'opensteer.meetings'

    def ready(self):
        import opensteer.meetings.signals  # noqa F401
