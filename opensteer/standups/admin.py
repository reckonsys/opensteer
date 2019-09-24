from django.contrib import admin
from opensteer.standups.models import Standup, StandupResponse

admin.site.register(Standup)
admin.site.register(StandupResponse)
