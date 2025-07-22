"""
This file defines how Tbl_observing_block model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin

# Local application imports
from ..models import Tbl_observing_block


@admin.register(Tbl_observing_block)
class ObservingBlockAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "obs_run", "description", "start_time", "end_time", ]}),
        ("Observation Information", {"fields": [
            "observation_mode", "filters", "exposure_time", "seeing", "weather_conditions", "target"]}),
        ("Additional Data", {"fields": [
            "comments"]}),]

    # Multi-select widget for targets
    filter_horizontal = ['target']
