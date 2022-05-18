from django.contrib import admin
from django.urls import path, re_path, include
from main.views import index

from agency.views import metabase_embed
from user.views import user_json, logout_ajax, complete_registration
import metabase.forms  # noqa

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("^$", index),
    re_path("^(auth|registration)", index),
    path("api/auth/user.json", user_json),
    path("api/auth/logout/", logout_ajax),
    path("api/registration/complete/<str:activation_key>/", complete_registration),
    path("api/metabase/", metabase_embed),
    re_path("", include("unrest.schema.urls")),
]
