from django.contrib import admin
from opensteer.teams.models import Team, Member, Question

admin.site.register(Team)
admin.site.register(Member)
admin.site.register(Question)
