import uuid

from config.settings.base import TIME_ZONE
from tenant_schemas.models import TenantMixin

from django.core.validators import MaxValueValidator
from django.db.models import (
    Model, DateTimeField, UUIDField, CharField, ForeignKey, CASCADE,
    PositiveSmallIntegerField as PSIF)

from opensteer.core.utils import (
    to_server_tz as _to_server_tz, to_company_tz as _to_company_tz, TIMEZONES)
from opensteer.core.choices import DayOfWeek


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TenantMixin):
    # default true, schema will be automatically created
    # and synced when it is saved
    auto_create_schema = True
    name = CharField(max_length=100, unique=True)
    meeting_hour = PSIF(validators=[MaxValueValidator(23)])
    meeting_minute = PSIF(validators=[MaxValueValidator(59)])
    timezone = CharField(max_length=32, default=TIME_ZONE, choices=TIMEZONES)
    checkin_day = PSIF(
        validators=[MaxValueValidator(len(DayOfWeek.CHOICES))],
        default=DayOfWeek.THURSDAY, choices=DayOfWeek.CHOICES)

    def to_server_tz(self):
        '''
        WARNING: Only call this on while saving the form.
        Calling this method more than required will corrupt the data.
        '''
        self.meeting_hour, self.meeting_minute, self.checkin_day = _to_server_tz(
            self.meeting_hour, self.meeting_minute, self.timezone, self.checkin_day)

    def to_company_tz(self):
        '''
        WARNING: Never call save() after calling this. This method is only
        intended convert the data back to organization-time so that it can
        be sent to OrganizationForm's initial data
        '''
        self.meeting_hour, self.meeting_minute, self.checkin_day = _to_company_tz(
            self.meeting_hour, self.meeting_minute, self.timezone, self.checkin_day)

    def __str__(self):
        return self.name


class CompanyBaseModel(BaseModel):
    company = ForeignKey(Company, on_delete=CASCADE)

    class Meta:
        abstract = True
