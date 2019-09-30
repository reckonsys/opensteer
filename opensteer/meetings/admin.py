from django.contrib import admin
from opensteer.meetings.models import Standup, Checkin, Submission, Response

admin.site.register(Standup)
admin.site.register(Checkin)
admin.site.register(Submission)
admin.site.register(Response)
