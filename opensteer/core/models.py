import uuid

from django.contrib.postgres.fields import JSONField
from django.db.models import (
    Model, DateTimeField, UUIDField, CharField, BooleanField,
    PositiveSmallIntegerField as PSIF)

from opensteer.core.choices import QuestionKind, QuestionCategory


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(BaseModel):
    data = JSONField(default=dict, blank=True)
    title = CharField(max_length=200, unique=True)
    is_active = BooleanField(default=True)
    is_mandatory = BooleanField(default=True)
    kind = PSIF(default=QuestionKind.TEXT, choices=QuestionKind.CHOICES)
    category = PSIF(
        default=QuestionCategory.STANDUP, choices=QuestionCategory.CHOICES)

    def __str__(self):
        return self.title
