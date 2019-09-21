from django.core.validators import MaxValueValidator
from django.db.models import (
    ForeignKey, CASCADE, PositiveSmallIntegerField as PSIF)

from opensteer.core.models import BaseModel
from opensteer.teams.models import Team, Member


POKER_CHOICES = [(i, str(i)) for i in [1, 2, 3, 5, 8, 13, 20, 40]]


class Poker(BaseModel):
    team = ForeignKey(Team, on_delete=CASCADE, related_name='pokers')
    member = ForeignKey(Member, on_delete=CASCADE, related_name='pokers')
    point = PSIF(choices=POKER_CHOICES, validators=[MaxValueValidator(40)])

    class Meta:
        unique_together = ['team', 'member']
