"""
This file defines how Tbl_observing_block model is displayed and managed in the Django Admin interface.
"""

# Standard libraries
from datetime import timedelta

# Third-party libraries
from django.contrib import admin
from django.urls import path

# Local application imports
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_observing_block, Tbl_observing_run, Tbl_target
from ..utils import import_csv_file

# Process each row of the CSV when importing observing blocks
def process_observing_block_row(row, idx, errors):
    from datetime import datetime, time, timedelta

    # Required field: name, start_time
    name = row.get("name")
    start_time_str = row.get("start_time")

    if not name:
        errors.append(f"Row {idx}: 'name' field is empty, skipping")
        return None

    if not start_time_str:
        errors.append(f"Row {idx}: 'start_time' field is empty, skipping")
        return None

    # Parse start_time (expecting 'YYYY-MM-DD HH:MM:SS')
    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        errors.append(f"Row {idx}: invalid start_time '{start_time_str}', skipping")
        return None

    # Parse optional end_time (only HH:MM:SS)
    end_time_str = row.get("end_time")
    end_time = None
    if end_time_str:
        try:
            end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        except ValueError:
            errors.append(f"Row {idx}: invalid end_time '{end_time_str}', ignoring")

    # Lookup foreign key obs_run by name
    obs_run_name = row.get("obs_run")
    obs_run_obj = None
    if obs_run_name:
        obs_run_obj = Tbl_observing_run.objects.filter(name=obs_run_name).first()
        if not obs_run_obj:
            errors.append(f"Row {idx}: Observing Run with name='{obs_run_name}' not found, skipping")
            return None

    # Create or update observing block by name
    obj, created_flag = Tbl_observing_block.objects.update_or_create(
        name=name,
        defaults={
            "obs_run": obs_run_obj,
            "description": row.get("description", ""),
            "start_time": start_time,
            "end_time": end_time,
            "observation_mode": row.get("observation_mode", "photometry"),
            "filters": row.get("filters", ""),
            "exposure_time": None,  # to parse below
            "seeing": None,         # to parse below
            "weather_conditions": row.get("weather_conditions", ""),
            "comments": row.get("comments", ""),
        }
    )

    # Parse exposure_time (seconds) as duration
    exposure_time_str = row.get("exposure_time")
    if exposure_time_str:
        try:
            seconds = float(exposure_time_str)
            obj.exposure_time = timedelta(seconds=seconds)
        except ValueError:
            errors.append(f"Row {idx}: invalid exposure_time '{exposure_time_str}', ignoring")
            obj.exposure_time = None

    # Parse seeing (float)
    seeing_str = row.get("seeing")
    if seeing_str:
        try:
            obj.seeing = float(seeing_str)
        except ValueError:
            errors.append(f"Row {idx}: invalid seeing '{seeing_str}', ignoring")
            obj.seeing = None

    # Save after modifying exposure_time and seeing
    obj.save()

    # Handle many-to-many target field (comma separated names)
    targets_str = row.get("target")
    if targets_str:
        target_names = [t.strip() for t in targets_str.split(",") if t.strip()]
        targets_qs = Tbl_target.objects.filter(name__in=target_names)
        if len(target_names) != targets_qs.count():
            missing = set(target_names) - set(targets_qs.values_list("name", flat=True))
            errors.append(f"Row {idx}: targets not found: {', '.join(missing)}")
        obj.target.set(targets_qs)
    else:
        obj.target.clear()

    # Handle allowed_groups many-to-many (comma separated group names)
    groups_str = row.get("allowed_groups")
    if groups_str:
        group_names = [g.strip() for g in groups_str.split(",") if g.strip()]
        from django.contrib.auth.models import Group
        groups_qs = Group.objects.filter(name__in=group_names)
        if len(group_names) != groups_qs.count():
            missing = set(group_names) - set(groups_qs.values_list("name", flat=True))
            errors.append(f"Row {idx}: allowed_groups not found: {', '.join(missing)}")
        obj.allowed_groups.set(groups_qs)
    else:
        obj.allowed_groups.clear()

    return created_flag


# Register the Tbl_observing_block model in the admin with custom settings
@admin.register(Tbl_observing_block)
class ObservingBlockAdmin(admin.ModelAdmin):

    # Group fields into sections in the admin form
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

    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/dwarfs4MOSAIC/tbl_observing_block_changelist.html"

    # Add a custom URL for CSV import view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_observing_block_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import using a helper function
    def import_csv(self, request):
        return import_csv_file(
            request,
            CsvImportForm,
            Tbl_observing_block,
            process_observing_block_row,
            title="Import observing blocks from CSV"
        )
