"""
This file defines how Tbl_observing_run model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin

# Local application imports
from ..models import Tbl_observing_run


@admin.register(Tbl_observing_run)
class ObservingRunAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "instrument", "start_date", "end_date", ]}), #targets
        ("Participants", {"fields": [
            "researchers"]}),
        ("Additional Data", {"fields": [
            "comments"]}),]

    # Multi-select widget for researchers
    filter_horizontal = ['researchers']
