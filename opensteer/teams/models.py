from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CharField, ForeignKey, CASCADE, PositiveSmallIntegerField as PSIF,
    BooleanField)

from opensteer.core.models import BaseModel
from opensteer.users.choices import UserRole
from opensteer.teams.utils import time_to_utc, time_to_local, TIMEZONES
from opensteer.teams.choices import QuestionKind, DayOfWeek, QuestionCategory

User = get_user_model()


class Organization(BaseModel):
    name = CharField(max_length=100)
    timezone = CharField(max_length=32, default='UTC', choices=TIMEZONES)
    standup_hour = PSIF(validators=[MaxValueValidator(23)])
    standup_minute = PSIF(validators=[MaxValueValidator(59)])
    checkin_hour = PSIF(validators=[MaxValueValidator(23)])
    checkin_minute = PSIF(validators=[MaxValueValidator(59)])
    checkin_day = PSIF(
        validators=[MaxValueValidator(6)],
        default=DayOfWeek.THURSDAY, choices=DayOfWeek.CHOICES)
    owner = ForeignKey(
        User, on_delete=CASCADE, related_name='owned_organizations')

    class Meta:
        unique_together = ['name', 'owner']

    def local_to_utc(self):
        '''
        WARNING: Only call this on while saving the form.
        Calling this method more than required will corrupt the data.
        '''
        self.standup_hour, self.standup_minute = time_to_utc(
            self.standup_hour, self.standup_minute, self.timezone)
        self.checkin_hour, self.checkin_minute = time_to_utc(
            self.checkin_hour, self.checkin_minute, self.timezone)

    def utc_to_local(self):
        '''
        WARNING: Never call save() after calling this. This method is only
        intended convert the data back to local-time so that it can
        be sent to OrganizationForm's initial data
        '''
        self.standup_hour, self.standup_minute = time_to_local(
            self.standup_hour, self.standup_minute, self.timezone)
        self.checkin_hour, self.checkin_minute = time_to_local(
            self.checkin_hour, self.checkin_minute, self.timezone)


class Question(BaseModel):
    title = CharField(max_length=200)
    is_active = BooleanField(default=True)
    options = ArrayField(CharField(max_length=100))
    kind = PSIF(default=QuestionKind.TEXT, choices=QuestionKind.CHOICES)
    organization = ForeignKey(
        Organization, on_delete=CASCADE, related_name='questions')
    category = PSIF(
        default=QuestionCategory.STANDUP, choices=QuestionCategory.CHOICES)


class Staff(BaseModel):
    title = CharField(max_length=100)
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)
    user = ForeignKey(User, on_delete=CASCADE, related_name='staffs')
    organization = ForeignKey(
        Organization, on_delete=CASCADE, related_name='staffs')

    class Meta:
        unique_together = ['user', 'organization']


class Team(BaseModel):
    name = CharField(max_length=100)
    organization = ForeignKey(
        Organization, on_delete=CASCADE, related_name='teams')

    class Meta:
        unique_together = ['name', 'organization']


class Member(BaseModel):
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)
    team = ForeignKey(Team, on_delete=CASCADE, related_name='members')
    staff = ForeignKey(Staff, on_delete=CASCADE, related_name='members')

    class Meta:
        unique_together = ['team', 'staff']
