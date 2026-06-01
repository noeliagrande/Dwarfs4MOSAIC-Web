"""
Utility module for shared Django application helpers.

Contains reusable functions for common backend tasks.
"""

# Standard libraries
import csv
from io import TextIOWrapper

# Third-party libraries
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import capfirst


# Handle CSV file upload and import rows via callback function.
# 'process_row_func' is called for each CSV row; it should return:
# - True if row created new entry,
# - False if updated existing entry,
# - None to skip the row.
def import_csv_file(request, form_class, model, process_row_func, title=None):
    # Handle CSV import via HTTP POST form submission
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            # Open uploaded CSV file as text with UTF-8 encoding
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)

            created = 0  # Count of newly created records
            updated = 0  # Count of updated records
            errors = []  # List to accumulate row errors

            # Process each CSV row starting at line 2 (assuming header is line 1)
            for idx, row in enumerate(reader, start=2):
                try:
                    # Call the user-provided function to process this row
                    # It should return True (created), False (updated), or None (skip)
                    created_flag = process_row_func(row, idx, errors)
                    if created_flag is None:
                        continue  # Skip this row if callback returns None
                    if created_flag:
                        created += 1
                    else:
                        updated += 1
                except Exception as e:
                    # Catch exceptions and store error with row number
                    errors.append(f"Row {idx}: error {e}")

            # Build success message with counts and any errors
            msg = f"Import completed: {created} created, {updated} updated."
            if errors:
                msg += f" Errors: {'; '.join(errors)}"

            # Show message to user and redirect back to previous page
            messages.success(request, msg)
            return redirect("..")
    else:
        # If not POST, just display empty form
        form = form_class()

    # Default page title if none provided
    if not title:
        title = f"Import {capfirst(model._meta.verbose_name_plural)} from CSV"

    # Render the CSV upload form template with context data
    context = {
        "form": form,
        "title": title,
        "opts": model._meta,
        "app_label": model._meta.app_label,
    }
    return render(request, "admin/csv_form.html", context)
