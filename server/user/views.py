from django.contrib.auth import logout, login
from django_registration.backends.activation.views import (
    ActivationView,
    ActivationError,
)

from main.http import JsonResponse


def user_json(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({})
    keys = ["id", "email", "is_superuser", "is_staff"]
    data = {key: getattr(user, key) for key in keys}
    data["username"] = data["email"]  # used for display on front end
    keys = ["id", "name"]
    data["agencies"] = [
        {key: getattr(agency, key) for key in keys} for agency in user.get_agencies()
    ]
    return JsonResponse({"user": data})


def logout_ajax(request):
    logout(request)
    return JsonResponse({})


def complete_registration(request, activation_key):
    view = ActivationView()
    try:
        user = view.activate(activation_key=activation_key)
    except ActivationError:
        error = "The registration you are using is expired."
        return JsonResponse({"error": error})
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return JsonResponse({"success": True})
