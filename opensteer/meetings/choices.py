from orm_choices import choices


@choices
class SubmissionStatus:
    class Meta:
        OPEN = [1, 'Open']
        CLOSED = [2, 'Closed']
