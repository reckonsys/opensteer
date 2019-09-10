from django.contrib import admin
from opensteer.teams.models import Organization, Staff, Team, Membership

admin.site.register(Team)
admin.site.register(Staff)
admin.site.register(Membership)
admin.site.register(Organization)
