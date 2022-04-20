from django.conf import settings
import jwt
from main.http import JsonResponse
import time

from agency.models import Agency


def metabase_embed(request):
    expires = round(time.time()) + (60 * 60)  # one hour in seconds
    params = {}
    if "cal_itp_id" in request.GET:
        agency = Agency.objects.get(id=request.GET["cal_itp_id"])
        params["cal_itp_id"] = agency.itp_id
    print(params)
    payload = {
        "resource": {"dashboard": int(request.GET.get("dashboard"))},
        "params": params,
        "exp": expires,
    }
    print(params)
    token = jwt.encode(payload, settings.METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{settings.METABASE_SITE_URL}/embed/dashboard/{token}"
    return JsonResponse({"iframe_url": iframe_url})
