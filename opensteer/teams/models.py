from config.settings.base import TIME_ZONE

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.contrib.postgres.fields import JSONField
from django.db.models import (
    CharField, ForeignKey, CASCADE, PositiveSmallIntegerField as PSIF,
    BooleanField, ManyToManyField)

from opensteer.core.models import BaseModel
from opensteer.users.choices import UserRole
from opensteer.teams.utils import (
    to_server_tz as _to_server_tz, to_org_tz as _to_org_tz, TIMEZONES)
from opensteer.teams.choices import QuestionKind, DayOfWeek, QuestionCategory

User = get_user_model()


class Organization(BaseModel):
    name = CharField(max_length=100)
    meeting_hour = PSIF(validators=[MaxValueValidator(23)])
    meeting_minute = PSIF(validators=[MaxValueValidator(59)])
    timezone = CharField(max_length=32, default=TIME_ZONE, choices=TIMEZONES)
    checkin_day = PSIF(
        validators=[MaxValueValidator(6)],
        default=DayOfWeek.THURSDAY, choices=DayOfWeek.CHOICES)
    owner = ForeignKey(
        User, on_delete=CASCADE, related_name='owned_organizations')

    class Meta:
        unique_together = ['name', 'owner']

    def to_server_tz(self):
        '''
        WARNING: Only call this on while saving the form.
        Calling this method more than required will corrupt the data.
        '''
        self.meeting_hour, self.meeting_minute, self.checkin_day = _to_server_tz(
            self.meeting_hour, self.meeting_minute, self.timezone, self.checkin_day)

    def to_org_tz(self):
        '''
        WARNING: Never call save() after calling this. This method is only
        intended convert the data back to organization-time so that it can
        be sent to OrganizationForm's initial data
        '''
        self.meeting_hour, self.meeting_minute, self.checkin_day = _to_org_tz(
            self.meeting_hour, self.meeting_minute, self.timezone, self.checkin_day)

    def __str__(self):
        return self.name


class Question(BaseModel):
    data = JSONField(default=dict, blank=True)
    title = CharField(max_length=200)
    is_active = BooleanField(default=True)
    is_mandatory = BooleanField(default=True)
    kind = PSIF(default=QuestionKind.TEXT, choices=QuestionKind.CHOICES)
    organization = ForeignKey(
        Organization, on_delete=CASCADE, related_name='questions')
    category = PSIF(
        default=QuestionCategory.STANDUP, choices=QuestionCategory.CHOICES)

    class Meta:
        unique_together = ['title', 'organization']

    def __str__(self):
        return self.title


class Staff(BaseModel):
    title = CharField(max_length=100)
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)
    user = ForeignKey(User, on_delete=CASCADE, related_name='staffs')
    organization = ForeignKey(
        Organization, on_delete=CASCADE, related_name='staffs')

    class Meta:
        unique_together = ['user', 'organization']

    def __str__(self):
        return f'u({self.user}) t({self.title})'


class Team(BaseModel):
    name = CharField(max_length=100)
    staffs = ManyToManyField(Staff, through='Member')
    organization = ForeignKey(
        Organization, on_delete=CASCADE, related_name='teams')

    class Meta:
        unique_together = ['name', 'organization']

    def __str__(self):
        return self.name


class Member(BaseModel):
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)
    team = ForeignKey(Team, on_delete=CASCADE, related_name='members')
    staff = ForeignKey(Staff, on_delete=CASCADE, related_name='members')

    class Meta:
        unique_together = ['team', 'staff']

    def __str__(self):
        return f'r({self.role}) t({self.team}) s({self.staff})'
