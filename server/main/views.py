from django.contrib.staticfiles import finders
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve
import os


@ensure_csrf_cookie
def index(request, *args, **kwargs):
    path = finders.find("index.html")
    return serve(request, os.path.basename(path), os.path.dirname(path))
