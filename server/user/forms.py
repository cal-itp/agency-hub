from django import forms
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple

from agency.models import Agency, AgencyUser
from .models import User
from unrest import schema


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


@schema.register
class LoginForm(forms.Form):
    user_can_POST = "ANY"
    email = forms.CharField(label="Email", max_length=150)
    password = forms.CharField(
        label="Password", max_length=128, widget=forms.PasswordInput,
    )

    def clean(self):
        User = get_user_model()
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if not email and password:
            return self.cleaned_data
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            self.user = user
            return self.cleaned_data
        raise forms.ValidationError(
            "Email and password do not match", code="password_mismatch"
        )

    def save(self, commit=True):
        backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, self.user, backend=backend)
