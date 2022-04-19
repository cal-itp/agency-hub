from django.contrib import admin
from django.urls import path, re_path, include
from unrest.views import index

from user.views import user_json, logout_ajax

# import unrest.user.forms

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("^$", index),
    re_path("^(auth)", index),
    path("api/auth/user.json", user_json),
    path("api/auth/logout/", logout_ajax),
    re_path("", include("unrest.schema.urls")),
]
