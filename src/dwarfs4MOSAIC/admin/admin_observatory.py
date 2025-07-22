"""
This file defines how Tbl_observatory model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin

# Local application imports
from ..forms import ObservatoryAdminForm
from ..models import Tbl_observatory


@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm
    empty_value_display = ""  # Show empty string instead of None

    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"]}),]
