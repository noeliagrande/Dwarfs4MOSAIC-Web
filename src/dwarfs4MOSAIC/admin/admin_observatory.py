"""
This file defines how Tbl_observatory model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.db.models.functions import Lower
from django.urls import path
from django.utils.html import format_html

# Local application imports
from ..forms import ObservatoryAdminForm
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_observatory
from ..utils import import_csv_file

# Process each row of the CSV when importing observatories
def process_observatory_row(row, idx, errors):
    # Get name, skip row if empty
    name = row.get("name")
    if not name:
        errors.append(f"Row {idx}: 'name' field is empty, skipping")
        return None

    # Update or create the observatory entry in the database
    obj, created_flag = Tbl_observatory.objects.update_or_create(
        name=name,
        defaults={
            "location": row.get("location", ""),
            "website": row.get("website", ""),
            "longitude": row.get("longitude") or 0,
            "latitude": row.get("latitude") or 0,
            "altitude": float(row.get("altitude") or 0),
        },
    )
    return created_flag

# Admin interface for Tbl_observatory with enhanced UI and CSV import support
@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):

    # Display main identifying fields for quick overview
    list_display = ("name", "location", "website_link")

    # Default ordering in changelist (case-insensitive + fallback)
    ordering = (Lower("name"),"name")

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

    # Custom ModelForm and shows empty values as empty strings instead of None
    form = ObservatoryAdminForm
    empty_value_display = ""

    # Group fields into logical sections for better usability
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            "longitude", "latitude", "altitude"]}),]

    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/dwarfs4MOSAIC/tbl_observatory_changelist.html"

    # Add a custom URL for CSV import view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_observatory_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import using a helper function
    def import_csv(self, request):
        return import_csv_file(
            request,
            CsvImportForm,
            Tbl_observatory,
            process_observatory_row,
            title="Import observatories from CSV"
        )

