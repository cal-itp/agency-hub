from django.conf import settings
import jwt
from main.http import JsonResponse
import time

from agency.models import Agency
from metabase.models import Dashboard


def metabase_embed(request):
    expires = round(time.time()) + (60 * 60)  # one hour in seconds
    params = {}
    dashboard = Dashboard.objects.get(id=request.GET.get("dashboard"))
    if dashboard.cal_itp_id:
        agency = Agency.objects.get(id=request.GET["cal_itp_id"])
        params["cal_itp_id"] = agency.itp_id
    if dashboard.feed_name:
        agency = Agency.objects.get(id=request.GET["cal_itp_id"])
        params["feed_name"] = "AC Transit (0)"
    payload = {
        "resource": {"dashboard": dashboard.metabase_id},
        "params": params,
        "exp": expires,
    }
    print(params)
    token = jwt.encode(payload, settings.METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{settings.METABASE_SITE_URL}/embed/dashboard/{token}"
    return JsonResponse({"iframe_url": iframe_url})
