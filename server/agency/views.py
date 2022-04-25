from django.conf import settings
import jwt
from main.http import JsonResponse
import time

from agency.models import Agency
from metabase.models import Dashboard


def metabase_embed(request):
    if not request.user.is_authenticated:
        error = "You must be logged in to view this resource."
        return JsonResponse({ "error": error }, status=401)
    expires = round(time.time()) + (60 * 60)  # one hour in seconds
    params = {}
    dashboard = Dashboard.objects.get(id=request.GET.get("dashboard"))
    agency = Agency.objects.get(id=request.GET["cal_itp_id"])
    if not agency in request.user.get_agencies():
        error = "You do not have the ability to access this agency."
        return JsonResponse({ "error": error }, status=403)
    if dashboard.cal_itp_id:
        params["cal_itp_id"] = agency.itp_id
    if dashboard.url_number:
        params["feed_name"] = f"{agency.name} ({request.GET['url_number']})"
    payload = {
        "resource": {"dashboard": dashboard.metabase_id},
        "params": params,
        "exp": expires,
    }
    token = jwt.encode(payload, settings.METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{settings.METABASE_SITE_URL}/embed/dashboard/{token}"
    return JsonResponse({"iframe_url": iframe_url})
