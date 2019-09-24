from datetime import date
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db.models import (
    CharField, ForeignKey, CASCADE, BooleanField, DateField,
    PositiveSmallIntegerField as PSIF)

from opensteer.core.models import BaseModel
from opensteer.teams.models import Team, Question, Member

User = get_user_model()
# Overview | teams | staffs | questions | settings


class Standup(BaseModel):
    date = DateField(default=date.today)
    is_active = BooleanField(default=True)
    team = ForeignKey(Team, on_delete=CASCADE, related_name='standups')

    class Meta:
        unique_together = ['team', 'date']

    @property
    def last_standup(self):
        return Standup.objects.filter(
            is_active=False, team=self.team).order_by(
                'date', 'created_at').first()


class Checkin(BaseModel):
    is_active = BooleanField(default=True)
    year = PSIF(validators=[MaxValueValidator(2047)])
    week = PSIF(validators=[MaxValueValidator(53)])
    team = ForeignKey(Team, on_delete=CASCADE, related_name='checkins')

    class Meta:
        unique_together = ['team', 'year', 'week']

    @property
    def last_checkin(self):
        return Checkin.objects.filter(
            is_active=False, team=self.team).order_by(
                'year', 'week', 'created_at').first()


class Response(BaseModel):
    text = CharField(max_length=500)
    member = ForeignKey(Member, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)

    class Meta:
        abstract = True


class StandupResponse(Response):
    standup = ForeignKey(
        Standup, on_delete=CASCADE, related_name='standup_responses')

    class Meta:
        unique_together = ['question', 'member', 'standup']


class CheckinResponse(Response):
    checkin = ForeignKey(
        Checkin, on_delete=CASCADE, related_name='checkin_responses')

    class Meta:
        unique_together = ['question', 'member', 'checkin']
