from django.views import View
from django.shortcuts import render

from opensteer.meetings.forms import SubmissionForm
from opensteer.meetings.models import Submission, Response


class SubmissionsView(View):
    template_name = 'meetings/submission_detail.html'

    def get_form(self, submission, *args):
        return SubmissionForm(submission, *args)

    def get(self, request, submission_id):
        submission = Submission.objects.get(id=submission_id)
        form = self.get_form(submission)
        return render(
            request, self.template_name, {
                'submission': submission, 'form': form})

    def post(self, request, submission_id):
        submission = Submission.objects.get(id=submission_id)
        form = self.get_form(submission, request.POST)
        if not form.is_valid():
            return render(
                request, self.template_name, {
                    'submission': submission, 'form': form})
        for question_id, text in form.cleaned_data.items():
            Response.objects.create(
                submission_id=submission_id, question_id=question_id, text=text)
        submission.submit()
        return render(
            request, self.template_name, {
                'submission': submission, 'form': form})
