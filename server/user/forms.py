from django import forms
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.http import urlsafe_base64_decode

from django_registration.backends.activation.views import RegistrationView


from agency.models import Agency, AgencyUser
from .models import User
from unrest import schema


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


@schema.register
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


@schema.register
class PasswordResetForm(PasswordResetForm):
    user_can_POST = "ALL"

    # the django password reset form uses a bunch of kwargs on save, making it very non-standard
    # we hack them in here so that this plays nice with the rest of the schema form flow
    def save(self, *args, **kwargs):
        kwargs["request"] = self.request
        return super().save(*args, **kwargs)


@schema.register
class FirstPasswordForm(SetPasswordForm):
    user_can_POST = "AUTH"

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.fields["new_password1"].help_text = None
        self.fields["new_password2"].label = "Confirm Password"

    def save(self, *args, **kwargs):
        self.user = self.request.user
        super().save(*args, **kwargs)

        # Changing a users password loggs them out
        user = get_user_model().objects.get(id=self.user.id)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return user


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


@schema.register
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
