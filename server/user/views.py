from django.http import JsonResponse
from django.contrib.auth import logout


def user_json(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({})
    keys = ["id", "username", "email", "is_superuser", "is_staff"]
    return JsonResponse({"user": {k: getattr(user, k) for k in keys}})


def logout_ajax(request):
    logout(request)
    return JsonResponse({})
