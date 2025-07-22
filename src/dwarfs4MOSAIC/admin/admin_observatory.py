"""
This file defines how Tbl_observatory model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.urls import path

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
            "longitude": float(row.get("longitude") or 0),
            "latitude": float(row.get("latitude") or 0),
            "altitude": float(row.get("altitude") or 0),
        },
    )
    return created_flag

# Register the Tbl_observatory model in the admin with custom settings
@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm
    empty_value_display = ""  # Show empty string instead of None

    # Group fields into sections in the admin form
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"]}),]

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

