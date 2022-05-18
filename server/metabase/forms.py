from django import forms
import unrest_schema

from metabase.models import Dashboard


@unrest_schema.register
class DashboardForm(forms.ModelForm):
    user_can_LIST = "ALL"

    class Meta:
        model = Dashboard
        fields = ["name", "cal_itp_id", "url_number"]
