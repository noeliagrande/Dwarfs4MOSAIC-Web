"""
Custom form fields
"""

# Third-party libraries
from django import forms

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
