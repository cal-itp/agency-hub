from django import forms
from unrest import schema

from metabase.models import Dashboard


@schema.register
class DashboardForm(forms.ModelForm):
    user_can_LIST = "ALL"

    class Meta:
        model = Dashboard
        fields = ["name"]
