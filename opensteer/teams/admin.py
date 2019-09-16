from django.contrib import admin
from opensteer.teams.models import Organization, Staff, Team, Member, Question

admin.site.register(Team)
admin.site.register(Staff)
admin.site.register(Member)
admin.site.register(Question)
admin.site.register(Organization)
