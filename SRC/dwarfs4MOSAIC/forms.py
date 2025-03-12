from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Tbl_observatory

class ObservatoryAdminForm(forms.ModelForm):
    # Longitude: must be between -180 and 180 degrees
    longitude_ew = forms.ChoiceField(
        choices=[('', ''), ('E', 'E'), ('W', 'W')],
        required=False,
        label="E/W",
    )
    longitude_deg = forms.IntegerField(
        required=False,
        label="degrees",
        validators=[MinValueValidator(0), MaxValueValidator(180)]
    )
    longitude_min = forms.IntegerField(
        required=False,
        label="minutes",
        validators=[MinValueValidator(0), MaxValueValidator(59)]
    )
    longitude_sec = forms.FloatField(
        required=False,
        label="seconds",
        validators=[MinValueValidator(0), MaxValueValidator(59)]
    )

    # Latitude: must be between -90 and 90 degrees
    latitude_ns = forms.ChoiceField(
        choices=[('', ''), ('N', 'N'), ('S', 'S')],
        required=False,
        label="N/S"
    )
    latitude_deg = forms.IntegerField(
        required=False,
        label="degrees",
        validators=[MinValueValidator(0), MaxValueValidator(90)]
    )
    latitude_min = forms.IntegerField(
        required=False,
        label="minutes",
        validators=[MinValueValidator(0), MaxValueValidator(59)]
    )
    latitude_sec = forms.FloatField(
        required=False,
        label="seconds",
        validators=[MinValueValidator(0), MaxValueValidator(59)]
    )

    class Meta:
        model = Tbl_observatory
        fields = '__all__'

    # Shows init values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get longitude and latitude
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

        # It is allowed not to define coordinates (all fields empty).
        if all(data in [None, ''] for data in [longitude_ew, longitude_deg, longitude_min, longitude_sec,
                                         latitude_ns, latitude_deg, latitude_min, latitude_sec]):
            cleaned_data['longitude'] = None
            cleaned_data['latitude'] = None
            self.instance.longitude = None
            self.instance.latitude = None
            return cleaned_data

        # If a field is defined, all fields must be defined.
        if any(data in [None, ''] for data in [longitude_ew, longitude_deg, longitude_min, longitude_sec]):
            raise ValidationError("Three longitude fields must be provided.")

        if any(data in [None, ''] for data in [latitude_ns, latitude_deg, latitude_min, latitude_sec]):
            raise ValidationError("Three latitude fields must be provided.")

        # Convert longitude and latitude to decimal and validate range
        longitude = longitude_deg + longitude_min / 60 + longitude_sec / 3600
        if longitude > 180:
            raise ValidationError("Longitude must be in the range [0, 180].")
        if longitude_ew == 'W': longitude = -longitude
        cleaned_data['longitude'] = longitude
        self.instance.longitude = longitude

        latitude = latitude_deg + latitude_min / 60 + latitude_sec / 3600
        if latitude > 90:
            raise ValidationError("Latitude must be in the range [0, 90].")
        if latitude_ns == 'S': latitude = -latitude
        cleaned_data['latitude'] = latitude
        self.instance.latitude = latitude

        return cleaned_data
