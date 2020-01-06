from django.urls import reverse
from django.db.models import CharField, PositiveSmallIntegerField as PSIF
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from opensteer.users.choices import UserRole


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    title = CharField(max_length=100)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    role = PSIF(default=UserRole.REGULAR, choices=UserRole.CHOICES)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
