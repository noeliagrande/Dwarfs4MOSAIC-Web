"""
Django admin forms for managing custom validation, display, and data processing
for the observatory, researcher, and target models.

Includes:
- Custom handling of geographic coordinates (longitude and latitude) for observatories.
- Validation to ensure unique assignment of users to researchers.
- Support for uploading multiple files and images associated with targets.
"""

import os

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe

from .models import Tbl_observatory, Tbl_researcher, Tbl_target
from django.contrib.auth.models import User

from django.conf import settings
from django.urls import reverse


# Form for observatory admin with detailed longitude and latitude input fields.
# Longitude and latitude are split into direction (E/W, N/S), degrees, minutes, and seconds.
# Includes conversion between decimal degrees and DMS, and validation of input completeness and range.
class ObservatoryAdminForm(forms.ModelForm):
    # Longitude components
    longitude_ew = forms.ChoiceField(
        choices=[('', ''), ('E', 'E'), ('W', 'W')],
        required=False,
        label="",
        help_text="direction"
    )
    longitude_deg = forms.IntegerField(
        required=False,
        label="Longitude",
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        widget=TextInput(attrs={'style': 'width: 50px;'}),
        help_text="degrees"
    )
    longitude_min = forms.IntegerField(
        required=False,
        label="",
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        widget=TextInput(attrs={'style': 'width: 50px;'}),
        help_text="minutes"
    )
    longitude_sec = forms.FloatField(
        required=False,
        label="",
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        widget=TextInput(attrs={'style': 'width: 50px;'}),
        help_text="seconds"
    )

    # Latitude components
    latitude_ns = forms.ChoiceField(
        choices=[('', ''), ('N', 'N'), ('S', 'S')],
        required=False,
        label="",
        help_text="direction"
    )
    latitude_deg = forms.IntegerField(
        required=False,
        label="Latitude",
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        widget=TextInput(attrs={'style': 'width: 50px;'}),
        help_text="degrees"
    )
    latitude_min = forms.IntegerField(
        required=False,
        label="",
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        widget=TextInput(attrs={'style': 'width: 50px;'}),
        help_text="minutes"
    )
    latitude_sec = forms.FloatField(
        required=False,
        label="",
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        widget=TextInput(attrs={'style': 'width: 50px;'}),
        help_text="seconds"
    )

    class Meta:
        model = Tbl_observatory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize longitude and latitude fields from decimal values on instance
        if self.instance.longitude is not None:
            # Convert longitude to deg, min, sec
            longitude_deg, remainder = divmod(abs(self.instance.longitude), 1)
            longitude_min, longitude_sec = divmod(remainder * 60, 1)
            longitude_sec *= 60
            self.fields['longitude_deg'].initial = int(longitude_deg)
            self.fields['longitude_min'].initial = int(longitude_min)
            self.fields['longitude_sec'].initial = round(longitude_sec, 2)
            self.fields['longitude_ew'].initial = 'W' if self.instance.longitude < 0 else 'E'

        if self.instance.latitude is not None:
            # Convert latitude to deg, min, sec
            latitude_deg, remainder = divmod(abs(self.instance.latitude), 1)
            latitude_min, latitude_sec = divmod(remainder * 60, 1)
            latitude_sec *= 60
            self.fields['latitude_deg'].initial = int(latitude_deg)
            self.fields['latitude_min'].initial = int(latitude_min)
            self.fields['latitude_sec'].initial = round(latitude_sec, 2)
            self.fields['latitude_ns'].initial = 'S' if self.instance.latitude < 0 else 'N'

    def clean(self):
        cleaned_data = super().clean()

        longitude_ew = cleaned_data.get('longitude_ew')
        longitude_deg = cleaned_data.get('longitude_deg')
        longitude_min = cleaned_data.get('longitude_min')
        longitude_sec = cleaned_data.get('longitude_sec')

        latitude_ns = cleaned_data.get('latitude_ns')
        latitude_deg = cleaned_data.get('latitude_deg')
        latitude_min = cleaned_data.get('latitude_min')
        latitude_sec = cleaned_data.get('latitude_sec')

        # Allow all coordinate fields to be empty (no coordinates provided)
        if all(data in [None, ''] for data in [longitude_ew, longitude_deg, longitude_min, longitude_sec,
                                         latitude_ns, latitude_deg, latitude_min, latitude_sec]):
            cleaned_data['longitude'] = None
            cleaned_data['latitude'] = None
            self.instance.longitude = None
            self.instance.latitude = None
            return cleaned_data

        # If any longitude field is provided, all must be provided
        if any(data in [None, ''] for data in [longitude_ew, longitude_deg, longitude_min, longitude_sec]):
            raise ValidationError("Three longitude fields must be provided.")

        # If any latitude field is provided, all must be provided
        if any(data in [None, ''] for data in [latitude_ns, latitude_deg, latitude_min, latitude_sec]):
            raise ValidationError("Three latitude fields must be provided.")

        # Convert longitude to decimal degrees and validate range
        longitude = longitude_deg + longitude_min / 60 + longitude_sec / 3600
        if longitude > 180:
            raise ValidationError("Longitude must be in the range [0, 180].")
        if longitude_ew == 'W': longitude = -longitude
        cleaned_data['longitude'] = longitude
        self.instance.longitude = longitude

        # Convert latitude to decimal degrees and validate range
        latitude = latitude_deg + latitude_min / 60 + latitude_sec / 3600
        if latitude > 90:
            raise ValidationError("Latitude must be in the range [0, 90].")
        if latitude_ns == 'S': latitude = -latitude
        cleaned_data['latitude'] = latitude
        self.instance.latitude = latitude

        return cleaned_data


# Custom widget allowing multiple file selection
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# FileField subclass to handle multiple file uploads and validation
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

# Form for target admin to support uploading an image and multiple data files,
# with options to delete current image and display current files.
class TargetAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        label="Image",
    )

    upload_datafiles = MultipleFileField(
        required=False,
        label="Data files",
    )

    delete_image = forms.BooleanField(required=False, label="No image")

    delete_files = forms.CharField(
        required=False,
        label="",
        widget=forms.widgets.TextInput(attrs={
            "type": "button",
            "value": "Delete files",
            "style": "background-color: #cc3300; color: white; padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer;",
        })
    )

    class Meta:
        model = Tbl_target
        exclude = ['image', 'datafiles_path']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show current image name if editing an existing target with an image
        if self.instance and self.instance.pk:
            #if self.instance.image:
            self.fields['upload_image'].help_text = mark_safe(
                f"<strong>Current image:</strong> {self.instance.image_name}"
            )

            # List current data files if path exists
            if self.instance.datafiles_path:
                files = []
                try:
                    full_path = os.path.join(settings.MEDIA_ROOT, self.instance.datafiles_path)
                    if os.path.exists(full_path):
                        files = os.listdir(full_path)
                except Exception as e:
                    files = [f"(Failed to access: {e})"]

                if files:
                    file_list = "<ul>" + "".join(f"<li>{f}</li>" for f in files) + "</ul>"
                    self.fields['delete_files'].widget.attrs['onclick'] = \
                        f"window.location.href='/delete_files/{self.instance.pk}/';"

                else:
                    file_list = "No files found"
                    if 'delete_files' in self.fields:
                        self.fields['delete_files'].widget = forms.HiddenInput()

                self.fields['upload_datafiles'].help_text = mark_safe(
                    f"<strong>Current data files:</strong><br>{file_list}"
                )
