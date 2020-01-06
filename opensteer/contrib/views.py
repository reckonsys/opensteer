from django.shortcuts import render

from opensteer.meetings.models import Submission
from opensteer.meetings.choices import SubmissionStatus


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {})
    submissions = Submission.objects.filter(
        member__user_id=request.user.id, status=SubmissionStatus.OPEN)
    return render(request, 'index.html', {'submissions': submissions})
