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

    @property
    def last_checkin(self):
        return Checkin.objects.filter(
            is_active=False, team=self.team).order_by(
                'year', 'week_of_year', 'created_at').first()


class CheckinResponse(BaseModel):
    text = CharField(max_length=500)
    checkin = ForeignKey(
        Checkin, on_delete=CASCADE, related_name='checkin_responses')
    member = ForeignKey(
        Member, on_delete=CASCADE, related_name='checkin_responses')
    question = ForeignKey(
        Question, on_delete=CASCADE, related_name='checkin_responses')

    class Meta:
        unique_together = ['question', 'member', 'checkin']
