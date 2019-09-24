from django.contrib import admin
from opensteer.checkins.models import Checkin, CheckinResponse

admin.site.register(Checkin)
admin.site.register(CheckinResponse)
