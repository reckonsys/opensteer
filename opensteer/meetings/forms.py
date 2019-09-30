from django.forms import Form, CharField, Textarea


class SubmissionForm(Form):

    def __init__(self, submission, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        for question in submission.get_questions():
            self.fields[str(question.id)] = CharField(
                widget=Textarea, label=question.title,
                required=question.is_mandatory)
