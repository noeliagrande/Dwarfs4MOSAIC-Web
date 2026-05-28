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
from ..constants import (
    COORDINATE_WIDTH,
    DROPBOX_WIDTH,
    NAME_WIDTH,
    NUMBER_WIDTH,
    REDSHIFT_WIDTH,
    TEXT_AREA,
    URL_WIDTH,
)
from ..models import Tbl_target
from .widgets.custom_widgets import SingleFileField, MultipleFileField


class TargetAdminForm(forms.ModelForm):

    upload_image = SingleFileField(
        required    = False,
        label       = "Image",
    )

    upload_datafiles = MultipleFileField(
        required    = False,
        label       = "Data files",
    )

    delete_image = forms.BooleanField(required=False, label="Delete image")

    # Field for selecting data files to delete
    datafiles = forms.MultipleChoiceField(
        required    = False,
        label       = "",
        help_text   = "Data files that will be deleted. "
                      "Hold down “Control”, or “Command” on a Mac, to select more than one.",
        widget      = FilteredSelectMultiple("data files to delete", is_stacked=False)
    )

    class Meta:
        model = Tbl_target
        exclude = ['image', 'datafiles_path']

        # visual sizes
        common_style = {'style': 'width:80px;'}

        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'size': NAME_WIDTH}),

            # General Information
            'type'              : forms.Select(attrs={'style': f'width: {DROPBOX_WIDTH}px;'}),
            'right_ascension'   : forms.TextInput(attrs = {'size': COORDINATE_WIDTH}),
            'declination'       : forms.TextInput(attrs = {'size': COORDINATE_WIDTH}),
            'magnitude'         : forms.NumberInput(attrs = {'style': f'width: {NUMBER_WIDTH}px;'}),
            'redshift_value'    : forms.NumberInput(attrs = {'style': f'width: {REDSHIFT_WIDTH}px;'}),
            'redshift_error'    : forms.NumberInput(attrs={'style': f'width: {REDSHIFT_WIDTH}px;'}),
            'size'              : forms.NumberInput(attrs = {'style': f'width: {NUMBER_WIDTH}px;', 'min': '0'}),

            # Additional Data
            'semester': forms.TextInput(attrs = {'size': NAME_WIDTH}),
            'comments': forms.Textarea(attrs = TEXT_AREA),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Visual sizes
        # Adjust width here to preserve Django's default URLField widget behavior
        # without overriding the admin URL widget (current/change/clear links).
        self.fields['website'].widget.attrs.update({'style': f'width: {URL_WIDTH}px;'})
        self.fields['website'].widget.attrs.update({
            'style': 'width:1000px;'
        })

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
