import datetime
from django.conf import settings
from google.cloud import bigquery
import jwt
from main.http import JsonResponse
import time

from agency.models import Agency
from metabase.models import Dashboard


def metabase_embed(request):
    if not request.user.is_authenticated:
        error = "You must be logged in to view this resource."
        return JsonResponse({"error": error}, status=401)
    expires = round(time.time()) + (60 * 60)  # one hour in seconds
    params = {}
    dashboard = Dashboard.objects.get(id=request.GET.get("dashboard"))
    agency = Agency.objects.get(id=request.GET["agency_id"])
    if agency not in request.user.get_agencies():
        error = "You do not have the ability to access this agency."
        return JsonResponse({"error": error}, status=403)
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


def agency_notices(request, agency_id=None):
    agency = Agency.objects.get(id=agency_id)
    if agency not in request.user.get_agencies():
        error = "You do not have the ability to access this agency."
        return JsonResponse({"error": error}, status=403)

    client = bigquery.Client()
    validation_table = "cal-itp-data-infra.views.validation_fact_daily_feed_codes"
    dim_table = "cal-itp-data-infra.views.gtfs_schedule_dim_feeds"
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))

    query = f"""
--        SELECT *
        SELECT v.feed_key, v.date, v.n_notices, d.calitp_itp_id, d.calitp_url_number, d.calitp_agency_name, d.raw_gtfs_schedule_url
        FROM `{validation_table}` as v
        JOIN `{dim_table}` as d
        ON v.feed_key = d.feed_key
        WHERE (
            d.calitp_itp_id = {agency.itp_id} AND
            v.date >= "{yesterday}"
        )
    """
    query_job = client.query(query)

    feeds_by_key = {}
    for row in query_job.result():
        # Row values can be accessed by field name or index.
        feed_key, date, n_notices, itp_id, url_number, agency_name, raw_url = row
        if feed_key not in feeds_by_key:
            feeds_by_key[feed_key] = dict(
                feed_key=feed_key,
                itp_id=itp_id,
                agency_name=agency_name,
                raw_url=raw_url,
                url_number=url_number,
                notices=0,
            )
        feeds_by_key[feed_key]["notices"] += n_notices

    return JsonResponse({"feeds": list(feeds_by_key.values())})
