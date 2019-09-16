from django.contrib import admin
from opensteer.standups.models import Standup, StandupQuestion, StandupResponse

admin.site.register(Standup)
admin.site.register(StandupQuestion)
admin.site.register(StandupResponse)
