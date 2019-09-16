from datetime import date
from django.contrib.auth import get_user_model
from django.db.models import (
    CharField, ForeignKey, CASCADE, BooleanField, DateField)

from opensteer.core.models import BaseModel
from opensteer.teams.models import Team, Question, Member

User = get_user_model()
# Overview | teams | staffs | questions | settings


class Standup(BaseModel):
    date = DateField(default=date.today)
    is_active = BooleanField(default=True)
    team = ForeignKey(Team, on_delete=CASCADE)

    class Meta:
        unique_together = ['team', 'date']


class StandupQuestion(BaseModel):
    team = ForeignKey(Team, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)
    mandatory = BooleanField(default=True)

    class Meta:
        unique_together = ['team', 'question']


class StandupResponse (BaseModel):
    text = CharField(max_length=500)
    member = ForeignKey(Member, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)

    class Meta:
        unique_together = ['member', 'question']
