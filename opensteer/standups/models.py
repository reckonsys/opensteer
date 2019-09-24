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
    team = ForeignKey(Team, on_delete=CASCADE, related_name='standups')

    class Meta:
        unique_together = ['team', 'date']

    @property
    def last_standup(self):
        return Standup.objects.filter(
            is_active=False, team=self.team).order_by(
                'date', 'created_at').first()


class StandupResponse (BaseModel):
    text = CharField(max_length=500)
    standup = ForeignKey(
        Standup, on_delete=CASCADE, related_name='standup_responses')
    member = ForeignKey(
        Member, on_delete=CASCADE, related_name='standup_responses')
    question = ForeignKey(
        Question, on_delete=CASCADE, related_name='standup_responses')

    class Meta:
        unique_together = ['question', 'member', 'standup']
