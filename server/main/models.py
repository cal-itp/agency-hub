from django.db import models
from django_ulid.models import default, ULIDField

class BaseModel(models.Model):
    id = ULIDField(default=default, primary_key=True, editable=False)
    class Meta:
        abstract = True