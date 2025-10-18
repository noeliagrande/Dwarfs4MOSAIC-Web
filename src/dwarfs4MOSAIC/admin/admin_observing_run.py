"""
This file defines how Tbl_observing_run model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.urls import path

# Local application imports
from ..forms import ObservingRunAdminForm
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_observing_run, Tbl_instrument, Tbl_researcher
from ..utils import import_csv_file

# Process each row of the CSV when importing observing runs
def process_observing_run_row(row, idx, errors):
    # Required fields: name, start_date
    name = row.get("name")
    start_date_str = row.get("start_date")
    if not name:
        errors.append(f"Row {idx}: 'name' field is empty, skipping")
        return None
    if not start_date_str:
        errors.append(f"Row {idx}: 'start_date' field is empty, skipping")
        return None

    # Parse dates (start_date and optional end_date)
    from datetime import datetime
    date_format = "%Y-%m-%d"  # adjust if your CSV uses a different format

    try:
        start_date = datetime.strptime(start_date_str, date_format).date()
    except ValueError:
        errors.append(f"Row {idx}: invalid start_date '{start_date_str}', skipping")
        return None

    end_date_str = row.get("end_date")
    end_date = None
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, date_format).date()
        except ValueError:
            errors.append(f"Row {idx}: invalid end_date '{end_date_str}', ignoring")

    # Lookup instrument (foreign key)
    instrument_name = row.get("instrument")
    instrument_obj = None
    if instrument_name:
        instrument_obj = Tbl_instrument.objects.filter(name=instrument_name).first()
        if not instrument_obj:
            errors.append(f"Row {idx}: instrument '{instrument_name}' not found, skipping")
            return None

    # Create or update the observing run instance
    obj, created_flag = Tbl_observing_run.objects.update_or_create(
        name=name,
        defaults={
            "description": row.get("description", ""),
            "instrument": instrument_obj,
            "start_date": start_date,
            "end_date": end_date,
            "comments": row.get("comments", ""),
        },
    )

    # For many-to-many field 'researchers', update after creation/update
    researchers_str = row.get("researchers")  # assume CSV has comma-separated names
    if researchers_str:
        researcher_names = [r.strip() for r in researchers_str.split(",") if r.strip()]
        researchers = Tbl_researcher.objects.filter(name__in=researcher_names)
        if len(researcher_names) != researchers.count():
            missing = set(researcher_names) - set(researchers.values_list("name", flat=True))
            errors.append(f"Row {idx}: researchers not found: {', '.join(missing)}")
        obj.researchers.set(researchers)
    else:
        obj.researchers.clear()

    return created_flag



# Register the Tbl_observing_run model in the admin with custom settings
@admin.register(Tbl_observing_run)
class ObservingRunAdmin(admin.ModelAdmin):

    # Custom form
    form = ObservingRunAdminForm

    # Group fields into sections in the admin form
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

    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/dwarfs4MOSAIC/tbl_observing_run_changelist.html"

    # Add a custom URL for CSV import view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_observing_run_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import using a helper function
    def import_csv(self, request):
        return import_csv_file(
            request,
            CsvImportForm,
            Tbl_observing_run,
            process_observing_run_row,
            title="Import observing runs from CSV"
        )