from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CharField, ForeignKey, CASCADE, PositiveSmallIntegerField as PSIF,
    BooleanField)

from opensteer.core.models import BaseModel
from opensteer.users.choices import UserRole
from opensteer.teams.choices import QuestionKind, DayOfWeek
from opensteer.teams.utils import time_to_local, TIMEZONES

User = get_user_model()
# Overview | teams | staffs | questions | settings


class Organization(BaseModel):
    name = CharField(max_length=100)
    timezone = CharField(max_length=32, default='UTC', choices=TIMEZONES)
    standup_hour = PSIF(validators=[MaxValueValidator(59)])
    standup_minute = PSIF(validators=[MaxValueValidator(59)])
    checkin_hour = PSIF(validators=[MaxValueValidator(59)])
    checkin_minute = PSIF(validators=[MaxValueValidator(59)])
    checkin_day = PSIF(
        validators=[MaxValueValidator(6)],
        default=DayOfWeek.THURSDAY, choices=DayOfWeek.CHOICES)
    owner = ForeignKey(
        User, on_delete=CASCADE, related_name='owned_organizations')

    class Meta:
        unique_together = ['name', 'owner']

    def checkin_time(self):
        return time_to_local(
            self.checkin_hour, self.checkin_minute, self.timezone)

    def standup_time(self):
        return time_to_local(
            self.standup_hour, self.standup_minute, self.timezone)


class Question(BaseModel):
    title = CharField(max_length=200)
    is_active = BooleanField(default=True)
    options = ArrayField(CharField(max_length=100))
    organization = ForeignKey(Organization, on_delete=CASCADE)
    kind = PSIF(default=QuestionKind.TEXT, choices=QuestionKind.CHOICES)


class Staff(BaseModel):
    title = CharField(max_length=100)
    user = ForeignKey(User, on_delete=CASCADE)
    organization = ForeignKey(Organization, on_delete=CASCADE)
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)
    invited_by = ForeignKey(
        User, on_delete=CASCADE, related_name='invited_staffs')

    class Meta:
        unique_together = ['user', 'organization']


class Team(BaseModel):
    name = CharField(max_length=100)
    organization = ForeignKey(Organization, on_delete=CASCADE)

    class Meta:
        unique_together = ['name', 'organization']


class Member(BaseModel):
    team = ForeignKey(Team, on_delete=CASCADE)
    staff = ForeignKey(Staff, on_delete=CASCADE)
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)

    class Meta:
        unique_together = ['team', 'staff']
