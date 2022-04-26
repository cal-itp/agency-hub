from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django_ulid.models import default

from agency.models import Agency
from main.models import ULIDField
from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = ULIDField(default=default, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    affiliation = models.CharField(max_length=64, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_agencies(self):
        if self.is_staff:
            return Agency.objects.all()
        objs = self.agencyuser_set.all().select_related("agency")
        return [o.agency for o in objs]

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
