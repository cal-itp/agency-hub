from django.db import models
from django_ulid.models import default, ULIDField


class ULIDField(ULIDField):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('default', None)
        return name, path, args, kwargs


class BaseModel(models.Model):
    id = ULIDField(default=default, primary_key=True, editable=False)

    class Meta:
        abstract = True
