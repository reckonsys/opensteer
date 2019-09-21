from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db.models import (
    CharField, ForeignKey, CASCADE, BooleanField,
    PositiveSmallIntegerField as PSIF)

from opensteer.core.models import BaseModel
from opensteer.teams.models import Team, Question, Member

User = get_user_model()
# Overview | teams | staffs | questions | settings


class Checkin(BaseModel):
    is_active = BooleanField(default=True)
    year = PSIF(validators=[MaxValueValidator(2047)])
    week_of_year = PSIF(validators=[MaxValueValidator(52)])
    team = ForeignKey(Team, on_delete=CASCADE, related_name='checkins')

    class Meta:
        unique_together = ['team', 'year', 'week_of_year']


class CheckinQuestion(BaseModel):
    is_mandatory = BooleanField(default=True)
    team = ForeignKey(
        Team, on_delete=CASCADE, related_name='checkin_questions')
    question = ForeignKey(
        Question, on_delete=CASCADE, related_name='checkin_questions')

    class Meta:
        unique_together = ['team', 'question']


class CheckinResponse(BaseModel):
    text = CharField(max_length=500)
    member = ForeignKey(
        Member, on_delete=CASCADE, related_name='checkin_responses')
    question = ForeignKey(
        Question, on_delete=CASCADE, related_name='checkin_responses')

    class Meta:
        unique_together = ['member', 'question']
