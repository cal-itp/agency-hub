from django import forms
from django.contrib.auth import login, get_user_model, password_validation
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.http import urlsafe_base64_decode

from django_registration.backends.activation.views import RegistrationView


from agency.models import Agency, AgencyUser
from .models import User
import unrest_schema


class UserCreationForm(forms.ModelForm):
    agencies = forms.ModelMultipleChoiceField(
        queryset=Agency.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("tags", False),
    )

    def save(self, commit=False):
        user = super().save(commit=False)

        # send user registration email using django registration
        user.is_active = False
        view = RegistrationView()
        view.request = self.request
        view.send_activation_email(user)
        user.save()

        for agency in self.cleaned_data["agencies"]:
            AgencyUser.objects.create(user=user, agency=agency)
        return user

    class Meta:
        model = User
        fields = ("email", "agencies")


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


@unrest_schema.register
class LoginForm(forms.Form):
    user_can_POST = "ALL"
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


@unrest_schema.register
class PasswordResetForm(PasswordResetForm):
    user_can_POST = "ALL"

    # the django password reset form uses a bunch of kwargs on save, making it very non-standard
    # we hack them in here so that this plays nice with the rest of the schema form flow
    def save(self, *args, **kwargs):
        kwargs["request"] = self.request
        return super().save(*args, **kwargs)


@unrest_schema.register
class FirstPasswordForm(forms.ModelForm):
    user_can_GET = "SELF"
    user_can_PUT = "SELF"
    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch",
            )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.instance.set_password(password)
        if commit:
            self.instance.save()

        user_id = self.instance.id
        user = get_user_model().objects.get(id=user_id)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        return user

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "affiliation",
            "new_password1",
            "new_password2",
        ]


def get_reset_user(uidb64, token):
    User = get_user_model()
    ValidationError = forms.ValidationError
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        return None

    if default_token_generator.check_token(user, token):
        return user


@unrest_schema.register
class ResetSetPasswordForm(SetPasswordForm):
    user_can_POST = "ALL"

    # In django, token validation is done in the view and user is passed into the form
    # this does all that in clean instead to make it fit into schema form flow
    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.fields["new_password1"].help_text = None
        self.fields["new_password2"].label = "Confirm Password"

    def clean(self):
        uidb64 = self.request.session.get("reset-uidb64", "")
        token = self.request.session.get("reset-token", "")
        self.user = get_reset_user(uidb64, token)
        if not self.user:
            raise forms.ValidationError("This password reset token has expired")
        return self.cleaned_data

    def save(self, commit=True):
        # password reset token is invalid after save. Remove from session
        user = super().save(commit)
        self.request.session.pop("reset-uidb64", None)
        self.request.session.pop("reset-token", None)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return user
