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
from .widgets.value_with_error_widget import ValueWithErrorField

# Admin form for targets
class TargetAdminForm(forms.ModelForm):

    redshift = ValueWithErrorField(label="Redshift (z)")

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
        help_text="Data files that will be deleted. "
                  "Hold down “Control”, or “Command” on a Mac, to select more than one.",
        widget=FilteredSelectMultiple("data files to delete", is_stacked=False)
    )

    class Meta:
        model = Tbl_target
        exclude = ['image', 'datafiles_path']

        # visual sizes
        common_style = {'style': 'width:80px;'}

        fields = ['right_ascension', 'declination', 'magnitude', 'size', 'semester']
        widgets = {
            'right_ascension': forms.TextInput(attrs = common_style),
            'declination': forms.TextInput(attrs = common_style),
            'magnitude': forms.NumberInput(attrs = common_style),
            'size': forms.NumberInput(attrs = common_style),
            'semester': forms.TextInput(attrs = common_style),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the model has a redshift value, separate in value ± error
        if self.instance and self.instance.redshift:
            try:
                val, err = self.instance.redshift.split('±')
                self.fields['redshift'].initial = [float(val.strip()), float(err.strip())]
            except Exception:
                self.fields['redshift'].initial = [None, None]

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        redshift_data = self.cleaned_data.get('redshift')
        if redshift_data:
            value, error = redshift_data # Unpack the value and error from the redshift field

            # Ensure error is a non-negative number; if None, default to 0
            if error is not None:
                error = abs(error)
            else:
                error = 0

            instance.redshift = f"{value} ± {error}" # Store as a formatted string "value ± error" in the model field
        else:
            instance.redshift = '' # If no redshift was provided, store as an empty string
        if commit:
            instance.save()
        return instance