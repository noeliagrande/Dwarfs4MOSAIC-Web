"""
This file defines how Tbl_instrument model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.urls import path

# Local application imports
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_instrument, Tbl_telescope
from ..utils import import_csv_file

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
        },
    )
    return created_flag


# Register the Tbl_instrument model in the admin with custom settings
@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):

    # Group fields into sections in the admin form
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "tel_ins", "website", "status"]}),]

    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/dwarfs4MOSAIC/tbl_instrument_changelist.html"

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