"""
Admin form for targets, supports uploading images and multiple data files
with options to delete current image and display current files.
"""

# Standard libraries
import os

# Third-party libraries
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe

# Local application imports
from ..models import Tbl_target

# Custom widget for selecting a single file
class CustomSingleFileButton(forms.ClearableFileInput):
    template_name = 'dwarfs4MOSAIC/custom_widgets/custom_single_file_button.html'

# Custom widget for selecting multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# File field that uses the custom single file widget
class SingleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", CustomSingleFileButton())
        super().__init__(*args, **kwargs)

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


# Admin form for targets
class TargetAdminForm(forms.ModelForm):
    upload_image = SingleFileField(
        required=False,
        label="Image",
    )

    upload_datafiles = MultipleFileField(
        required=False,
        label="Data files",
    )

    delete_image = forms.BooleanField(required=False, label="Delete image")

    # Field for selecting data files to delete
    datafiles = forms.MultipleChoiceField(
        required=False,
        label="",
        widget=FilteredSelectMultiple("data files to delete", is_stacked=False)
    )

    class Meta:
        model = Tbl_target
        exclude = ['image', 'datafiles_path']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show current image name if editing an existing target with an image
        if self.instance and self.instance.pk:
            if self.instance.image_name:
                self.fields['upload_image'].help_text = mark_safe(
                    f"<strong>Current image:</strong> {self.instance.image_name}"
                )
            else:
                self.fields['upload_image'].help_text = None

            # List available data files if datafiles_path exists
            if self.instance.datafiles_path:
                files = []
                try:
                    files_path = os.path.join(settings.MEDIA_ROOT, self.instance.datafiles_path)
                    if os.path.exists(files_path):
                        files = sorted(os.listdir(files_path))
                except Exception as e:
                    files = [f"(Failed to access: {e})"]

                if files:
                    self.fields['datafiles'].choices = [(f, f) for f in files]
                else:
                    self.fields['datafiles'].choices = []
