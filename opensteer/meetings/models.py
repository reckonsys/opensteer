from datetime import date
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import (
    CharField, ForeignKey, CASCADE, BooleanField, DateField,
    PositiveSmallIntegerField as PSIF, UUIDField)

from opensteer.core.models import BaseModel
from opensteer.teams.choices import QuestionCategory
from opensteer.meetings.choices import SubmissionStatus
from opensteer.teams.models import Team, Question, Member

User = get_user_model()
# Overview | teams | staffs | questions | settings


class Meeting(BaseModel):
    is_active = BooleanField(default=True)

    class Meta:
        abstract = True

    def deactivate(self):
        self.is_active = False
        return self.save()


class Standup(Meeting):
    date = DateField(default=date.today)
    team = ForeignKey(Team, on_delete=CASCADE, related_name='standups')

    class Meta:
        unique_together = ['team', 'date']

    @property
    def last_standup(self):
        return Standup.objects.filter(
            is_active=False, team=self.team).order_by(
                'date', 'created_at').first()


class Checkin(Meeting):
    week = PSIF(validators=[MaxValueValidator(53)])
    year = PSIF(validators=[MaxValueValidator(2047)])
    team = ForeignKey(Team, on_delete=CASCADE, related_name='checkins')

    class Meta:
        unique_together = ['team', 'year', 'week']

    @property
    def last_checkin(self):
        return Checkin.objects.filter(
            is_active=False, team=self.team).order_by(
                'year', 'week', 'created_at').first()


class Submission(BaseModel):
    meeting_id = UUIDField()
    meeting_type = ForeignKey(ContentType, on_delete=CASCADE)
    meeting_object = GenericForeignKey('meeting_type', 'meeting_id')
    member = ForeignKey(Member, on_delete=CASCADE, related_name='submissions')
    status = PSIF(
        choices=SubmissionStatus.CHOICES, default=SubmissionStatus.OPEN)

    class Meta:
        unique_together = ['member', 'meeting_type', 'meeting_id']

    def is_open(self):
        return self.status == SubmissionStatus.OPEN

    def get_question_category(self):
        print(self.meeting_type.name)
        if self.meeting_type.name == 'standup':
            return QuestionCategory.STANDUP
        elif self.meeting_type.name == 'checkin':
            return QuestionCategory.CHECKIN
        raise NotImplementedError('Unknown meeeting type!')

    def get_questions(self):
        return Question.objects.filter(
            category=self.get_question_category(),
            organization=self.member.team.organization,
        )

    def close(self):
        self.status = SubmissionStatus.CLOSED
        self.save()


class Response(BaseModel):
    text = CharField(max_length=500)
    question = ForeignKey(Question, on_delete=CASCADE, related_name='responses')
    submission = ForeignKey(Submission, on_delete=CASCADE, related_name='responses')

    class Meta:
        unique_together = ['question', 'submission']
