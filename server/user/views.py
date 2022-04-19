from django.contrib.auth import logout

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
