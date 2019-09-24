from django.contrib import admin
from opensteer.meetings.models import (
    Standup, Checkin, StandupResponse, CheckinResponse)

admin.site.register(Standup)
admin.site.register(Checkin)
admin.site.register(StandupResponse)
admin.site.register(CheckinResponse)
