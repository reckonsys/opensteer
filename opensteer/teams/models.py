from django.contrib.auth import get_user_model
from django.db.models import (
    CharField, ForeignKey, CASCADE, BooleanField, ManyToManyField)

from opensteer.core.models import BaseModel

User = get_user_model()


class Team(BaseModel):
    name = CharField(max_length=100, unique=True)
    users = ManyToManyField(User, through='Member')

    def __str__(self):
        return self.name


class Member(BaseModel):
    is_reporter = BooleanField(default=True)
    team = ForeignKey(Team, on_delete=CASCADE, related_name='members')
    user = ForeignKey(User, on_delete=CASCADE, related_name='members')

    class Meta:
        unique_together = ['team', 'user']

    def __str__(self):
        return f't({self.team}) s({self.user}) reportee({self.is_reporter})'
