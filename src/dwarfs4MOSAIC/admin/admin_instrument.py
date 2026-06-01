"""
This file defines how Tbl_instrument model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.db.models.functions import Lower
from django.urls import path
from django.utils.html import format_html

# Local application imports
from . helpers import import_csv_file
from ..forms import InstrumentAdminForm
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_instrument, Tbl_telescope


# Process each row of the CSV when importing instruments
def process_instrument_row(row, idx, errors):
    # Get name, skip row if empty
    name = row.get("name")
    if not name:
        errors.append(f"Row {idx}: 'name' field is empty, skipping")
        return None

    # Get telescope by name, if provided
    tel_name = row.get("telescope")
    telescope = None
    if tel_name:
        telescope = Tbl_telescope.objects.filter(name=tel_name).first()
        if not telescope:
            errors.append(f"Row {idx}: telescope '{tel_name}' not found, skipping")
            return None

    # Update or create the instrument entry in the database
    obj, created_flag = Tbl_instrument.objects.update_or_create(
        name=name,
        defaults={
            "description": row.get("description", ""),
            "tel_ins": telescope,
            "status": row.get("status", "unknown"),
            "website": row.get("website", ""),
            "filters": row.get("filters", ""),
            "configuration": row.get("configuration", ""),
        },
    )
    return created_flag


# Admin interface for Tbl_instrument with enhanced UI and CSV import support
@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):

    # Display main identifying fields plus custom formatted columns for quick overview
    list_display = ("name", "description", "tel_ins", "status_colored", "website_link")

    # Sidebar filters for quick data segmentation in the admin changelist view
    list_filter = ("tel_ins", "status")

    # Default ordering in changelist (case-insensitive + fallback)
    ordering = (Lower("name"),"name")

    # Custom formatted status column (color-coded)
    @admin.display(description="status")
    def status_colored(self, obj):

        if obj.status == "inoperative":
            color = "red"
        elif obj.status == "maintenance":
            color = "#ff6200"
        else:
            color = "black"

        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.status
        )

    # External website link opening in a new tab
    @admin.display(description="website")
    def website_link(self, obj):

        if not obj.website:
            return "-"

        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
            obj.website,
            obj.website
        )

    # Custom ModelForm for validation and layout control
    form = InstrumentAdminForm

    # Group fields into logical sections for better usability
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "tel_ins", "website", "status"]}),
        ("Additional Data", {"fields": [
            "filters", "configuration"]}), ]


    # CSV import
    # ----------
    # CSV import functionality temporarily disabled.
    # The implementation is preserved for potential future reactivation.
    # To restore it, uncomment change_list_template line.

    # Override the change list template to add the custom "Import CSV" button
    # change_list_template = "admin/dwarfs4MOSAIC/tbl_instrument_changelist.html"

    # Add a custom URL for CSV import view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_instrument_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import using a helper function
    def import_csv(self, request):
        return import_csv_file(
            request,
            CsvImportForm,
            Tbl_instrument,
            process_instrument_row,
            title="Import instruments from CSV"
        )
