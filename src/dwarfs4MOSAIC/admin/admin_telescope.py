"""
This file defines how Tbl_telescope model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin

# Local application imports
from ..models import Tbl_telescope


@admin.register(Tbl_telescope)
class TelescopeAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": [
            "aperture"]}),]
