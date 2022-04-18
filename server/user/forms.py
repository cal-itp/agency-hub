from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple


from agency.models import Agency, AgencyUser
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    agencies = forms.ModelMultipleChoiceField(
        queryset=Agency.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("tags", False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["agencies"].initial = self.instance.get_agencies()

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        existing = list(user.get_agencies())
        for agency in self.cleaned_data["agencies"]:
            if agency in existing:
                existing.remove(agency)
            else:
                AgencyUser.objects.create(user=user, agency=agency)
        user.agencyuser_set.filter(agency__in=existing).delete()
        return user

    class Meta:
        model = User
        fields = ("email", "agencies")
