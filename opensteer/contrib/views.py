from django.db.models import Q
from django.shortcuts import render

from opensteer.teams.models import Organization


def index(request):
    organizations = None
    if request.user.is_authenticated:
        organizations = Organization.objects.filter(
            Q(staff__user__id=request.user.id) | Q(owner__id=request.user.id))
    ctx = {'organizations': organizations}
    return render(request, 'index.html', ctx)
