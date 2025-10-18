"""
This file defines how Tbl_telescope model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.urls import path

# Local application imports
from ..forms import TelescopeAdminForm
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_telescope, Tbl_observatory
from ..utils import import_csv_file

# Process each row of the CSV when importing telescopes
def process_telescope_row(row, idx, errors):
    # Get name, skip row if empty
    name = row.get("name")
    if not name:
        errors.append(f"Row {idx}: 'name' field is empty, skipping")
        return None

    # Get observatory by name, if provided
    obs_name = row.get("observatory")
    observatory = None
    if obs_name:
        observatory = Tbl_observatory.objects.filter(name=obs_name).first()
        if not observatory:
            errors.append(f"Row {idx}: observatory '{obs_name}' not found, skipping")
            return None

    # Update or create the telescope entry in the database
    obj, created_flag = Tbl_telescope.objects.update_or_create(
        name=name,
        defaults={
            "description": row.get("description", ""),
            "obs_tel": observatory,
            "owner": row.get("owner", ""),
            "aperture": float(row.get("aperture") or 0),
            "status": row.get("status", "unknown"),
            "website": row.get("website", ""),
        },
    )
    return created_flag


# Register the Tbl_telescope model in the admin with custom settings
@admin.register(Tbl_telescope)
class TelescopeAdmin(admin.ModelAdmin):
    # Custom form
    form = TelescopeAdminForm

    # Group fields into sections in the admin form
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": [
            "aperture"]}),]

    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/dwarfs4MOSAIC/tbl_telescope_changelist.html"

    # Add a custom URL for CSV import view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_telescope_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import using a helper function
    def import_csv(self, request):
        return import_csv_file(
            request,
            CsvImportForm,
            Tbl_telescope,
            process_telescope_row,
            title="Import telescopes from CSV"
        )