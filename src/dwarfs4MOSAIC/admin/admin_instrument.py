"""
This file defines how Tbl_instrument model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin

# Local application imports
from ..models import Tbl_instrument


@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "tel_ins", "website", "status"]}),]

