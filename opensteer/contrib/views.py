from django.db.models import Q
from django.shortcuts import render

from opensteer.teams.models import Organization
from opensteer.meetings.models import Submission
from opensteer.meetings.choices import SubmissionStatus


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {})
    organizations = Organization.objects.filter(
        Q(staffs__user__id=request.user.id) | Q(owner__id=request.user.id)
    ).order_by('id').distinct('id')
    submissions = Submission.objects.filter(
        member__staff__user_id=request.user.id, status=SubmissionStatus.OPEN)
    return render(request, 'index.html', {
        'submissions': submissions,
        'organizations': organizations,
    })
