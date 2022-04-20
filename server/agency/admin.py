from django.contrib import admin

from agency.models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "itp_id", "url_count"]
