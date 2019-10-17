
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db.models import (
    CharField, ForeignKey, CASCADE, PositiveSmallIntegerField as PSIF,
    BooleanField, ManyToManyField)

from opensteer.core.models import CompanyBaseModel
from opensteer.teams.choices import QuestionKind, QuestionCategory

User = get_user_model()


class Question(CompanyBaseModel):
    data = JSONField(default=dict, blank=True)
    title = CharField(max_length=200)
    is_active = BooleanField(default=True)
    is_mandatory = BooleanField(default=True)
    kind = PSIF(default=QuestionKind.TEXT, choices=QuestionKind.CHOICES)
    category = PSIF(
        default=QuestionCategory.STANDUP, choices=QuestionCategory.CHOICES)

    class Meta:
        unique_together = ['title', 'company_id']

    def __str__(self):
        return self.title


class Team(CompanyBaseModel):
    name = CharField(max_length=100)
    users = ManyToManyField(User, through='Member')

    class Meta:
        unique_together = ['name', 'company_id']

    def __str__(self):
        return self.name


class Member(CompanyBaseModel):
    is_reporter = BooleanField(default=True)
    team = ForeignKey(Team, on_delete=CASCADE, related_name='members')
    user = ForeignKey(User, on_delete=CASCADE, related_name='members')

    class Meta:
        unique_together = ['team', 'user']

    def __str__(self):
        return f'r({self.role}) t({self.team}) s({self.staff})'
