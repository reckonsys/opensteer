from django.contrib import admin
from opensteer.checkins.models import Checkin, CheckinQuestion, CheckinResponse

admin.site.register(Checkin)
admin.site.register(CheckinQuestion)
admin.site.register(CheckinResponse)
