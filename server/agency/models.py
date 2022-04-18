from django.conf import settings
from django.db import models
from main.models import BaseModel


class Agency(BaseModel):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    itp_id = models.IntegerField(unique=True)


class AgencyUser(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    agency = models.ForeignKey(Agency, models.CASCADE)
