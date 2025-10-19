"""
Form definition to handle CSV file upload for data import.
"""

# Third-party libraries
from django import forms

# Local application imports
from .widgets.custom_widgets import SingleFileField

# Form to upload a single CSV file for import
class CsvImportForm(forms.Form):

    csv_file = SingleFileField(
        required=False,
        label="CSV file:",
    )