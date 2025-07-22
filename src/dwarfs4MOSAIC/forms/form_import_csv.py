
# Third-party libraries
from django import forms

# Local application imports
from ..utils import SingleFileField

class CsvImportForm(forms.Form):

    csv_file = SingleFileField(
        required=False,
        label="CSV file",
    )