from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db.models import (
    CharField, ForeignKey, CASCADE, PositiveSmallIntegerField)

from opensteer.core.models import BaseModel
from opensteer.teams.choices import MembershipRole

User = get_user_model()


class Organization(BaseModel):
    name = CharField(_('Name of Organization'), blank=True, max_length=100)
    owner = ForeignKey(
        User, on_delete=CASCADE, related_name='owned_organizations')
    # staffs = ManyToManyField(
    #     User, through='Staff', through_fields=('user', 'organization'))

    class Meta:
        unique_together = ['name', 'owner']


class Staff(BaseModel):
    invite_reason = CharField(max_length=100)
    user = ForeignKey(User, on_delete=CASCADE)
    organization = ForeignKey(Organization, on_delete=CASCADE)
    invited_by = ForeignKey(
        User, on_delete=CASCADE, related_name='invited_staffs')

    class Meta:
        unique_together = ['user', 'organization']


class Team(BaseModel):
    organization = ForeignKey(Organization, on_delete=CASCADE)
    name = CharField(_('Name of Team'), blank=True, max_length=100)
    owner = ForeignKey(User, on_delete=CASCADE, related_name='owned_teams')
    # members = ManyToManyField(
    #     User, through='Membership', through_fields=('user', 'team'))

    class Meta:
        unique_together = ['name', 'organization']


class Membership(BaseModel):
    team = ForeignKey(Team, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    role = PositiveSmallIntegerField(
        default=MembershipRole.REGULAR, choices=MembershipRole.CHOICES)

    class Meta:
        unique_together = ['user', 'team']
