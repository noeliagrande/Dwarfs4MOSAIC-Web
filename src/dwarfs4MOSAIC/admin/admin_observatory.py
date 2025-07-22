"""
This file defines how Tbl_observatory model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
import csv
from io import TextIOWrapper

# Local application imports
from ..forms import ObservatoryAdminForm
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_observatory

@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm
    empty_value_display = ""  # Show empty string instead of None

    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"]}),]

    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/tbl_observatory_changelist.html"

    # Add a custom URL to handle CSV import
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_observatory_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import
    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
                reader = csv.DictReader(csv_file)
                created = 0
                updated = 0
                errors = []

                for idx, row in enumerate(reader, start=2):
                    name = row.get("name")
                    if not name:
                        errors.append(f"Row {idx}: 'name' field is empty, skipping")
                        continue
                    try:
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
                        if created_flag:
                            created += 1
                        else:
                            updated += 1
                    except Exception as e:
                        errors.append(f"Row {idx}: error {e}")
                msg = f"Import completed: {created} created, {updated} updated."
                if errors:
                    msg += f" Errors: {'; '.join(errors)}"
                self.message_user(request, msg, messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = {
            "form": form,
            "title": "Import observatories from CSV",
            "opts": self.model._meta,
            "app_label": self.model._meta.app_label,
        }
        return render(request, "admin/csv_form.html", context)