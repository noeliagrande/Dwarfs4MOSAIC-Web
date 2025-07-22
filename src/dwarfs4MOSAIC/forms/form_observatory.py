"""
Admin form for observatories with detailed longitude and latitude input fields.
Longitude and latitude are split into direction (E/W, N/S), degrees, minutes, and seconds.
Includes conversion between decimal degrees and DMS, and validation of input completeness and range.
"""

# Third-party libraries
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.widgets import TextInput

# Local application imports
from ..models import Tbl_observatory

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

        # Populate longitude and latitude fields from instance values
        if self.instance.longitude is not None:
            # Convert stored longitude (decimal degrees) to degrees, minutes, seconds
            longitude_deg, remainder = divmod(abs(self.instance.longitude), 1)
            longitude_min, longitude_sec = divmod(remainder * 60, 1)
            longitude_sec *= 60
            self.fields['longitude_deg'].initial = int(longitude_deg)
            self.fields['longitude_min'].initial = int(longitude_min)
            self.fields['longitude_sec'].initial = round(longitude_sec, 2)
            self.fields['longitude_ew'].initial = 'W' if self.instance.longitude < 0 else 'E'

        if self.instance.latitude is not None:
            # Convert stored latitude (decimal degrees) to degrees, minutes, seconds
            latitude_deg, remainder = divmod(abs(self.instance.latitude), 1)
            latitude_min, latitude_sec = divmod(remainder * 60, 1)
            latitude_sec *= 60
            self.fields['latitude_deg'].initial = int(latitude_deg)
            self.fields['latitude_min'].initial = int(latitude_min)
            self.fields['latitude_sec'].initial = round(latitude_sec, 2)
            self.fields['latitude_ns'].initial = 'S' if self.instance.latitude < 0 else 'N'

    def clean(self):
        # Validate and convert longitude and latitude input to decimal values
        cleaned_data = super().clean()

        longitude_ew = cleaned_data.get('longitude_ew')
        longitude_deg = cleaned_data.get('longitude_deg')
        longitude_min = cleaned_data.get('longitude_min')
        longitude_sec = cleaned_data.get('longitude_sec')

        latitude_ns = cleaned_data.get('latitude_ns')
        latitude_deg = cleaned_data.get('latitude_deg')
        latitude_min = cleaned_data.get('latitude_min')
        latitude_sec = cleaned_data.get('latitude_sec')

        # Allow all fields empty (no coordinates provided)
        if all(data in [None, ''] for data in [longitude_ew, longitude_deg, longitude_min, longitude_sec,
                                               latitude_ns, latitude_deg, latitude_min, latitude_sec]):
            cleaned_data['longitude'] = None
            cleaned_data['latitude'] = None
            self.instance.longitude = None
            self.instance.latitude = None
            return cleaned_data

        # Validate that all longitude fields are filled if any are provided
        if any(data in [None, ''] for data in [longitude_ew, longitude_deg, longitude_min, longitude_sec]):
            raise ValidationError("Three longitude fields must be provided.")

        # Validate that all latitude fields are filled if any are provided
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

