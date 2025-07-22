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
from ..utils import SingleFileField, MultipleFileField

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
