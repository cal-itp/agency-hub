from django.db import models
from main.models import BaseModel


class Dashboard(BaseModel):
    metabase_id = models.IntegerField()
    name = models.CharField(max_length=64)
    cal_itp_id = models.BooleanField()
    _ht = "Only used with GTFS Guidelines Date"
    url_number = models.BooleanField(help_text=_ht)

    def __str__(self):
        return self.name
