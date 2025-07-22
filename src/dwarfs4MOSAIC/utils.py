"""
Utility functions and custom form fields for database queries, file handling, and CSV imports.

Includes:
- Convert DB cursor results to list of dicts.
- List files in MEDIA_ROOT subfolders.
- Generate unique filenames to avoid overwriting.
- Sanitize filenames for safe filesystem use.
- Import CSV files with row processing callback.
- Custom Django form widgets and fields for single and multiple file uploads.
"""

# Standard libraries
import csv
import os
import re
import unicodedata
from io import TextIOWrapper

# Third-party libraries
from django import forms
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import capfirst


'''
---------------
   FUNCTIONS
---------------
'''

# Convert all rows from a DB cursor into a list of dictionaries.
# Each dictionary represents a row with column names as keys.
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# List files inside a directory relative to MEDIA_ROOT.
# Returns a list of filenames or empty list if directory does not exist.
def get_files(path):
    if not path:
        return []

    full_path = os.path.join(settings.MEDIA_ROOT, path)

    try:
        files = os.listdir(full_path)
        return files
    except FileNotFoundError:
        return []

# Generate a unique filename by adding a numeric suffix if needed.
# Example: file.txt → file (1).txt → file (2).txt, etc.
def get_unique_filename(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1

    return new_filename

# Sanitize a filename by:
# - Removing accents and special Unicode characters.
# - Keeping only letters, numbers, dashes, underscores, periods, and spaces.
# - Replacing spaces with underscores.
def sanitize_filename(name):
    # Normalize Unicode characters to ASCII equivalents (e.g., é → e, ñ → n)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

    # Remove invalid characters
    name = re.sub(r'[^\w\-. ]', '', name)

    # Replace spaces with underscores
    name = name.replace(' ', '_')

    return name


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


'''
--------------
   CLASSES
--------------
'''

# Custom widget for selecting a single file
class CustomSingleFileButton(forms.ClearableFileInput):
    template_name = 'dwarfs4MOSAIC/custom_widgets/custom_single_file_button.html'

# File field that uses the custom single file widget
class SingleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", CustomSingleFileButton())
        super().__init__(*args, **kwargs)

# Custom widget for selecting multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# Custom widget template for multiple file uploads
class CustomMultipleFileButton(MultipleFileInput):
    template_name = 'dwarfs4MOSAIC/custom_widgets/custom_multiple_file_button.html'

# File field that allows multiple file uploads
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", CustomMultipleFileButton())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Validate each uploaded file individually
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


