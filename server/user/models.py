from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django_ulid.models import default, ULIDField

from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = ULIDField(default=default, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_agencies(self):
        objs = self.agencyuser_set.all().select_related("agency")
        return [o.agency for o in objs]

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
