"""
Admin form for observatories with detailed longitude and latitude input fields.
Longitude and latitude are split into direction (E/W, N/S), degrees, minutes, and seconds.
Includes conversion between decimal degrees and DMS, and validation of input completeness and range.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..models import Tbl_observatory

class ObservatoryAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observatory

        # visual sizes
        common_style = {'style': 'width:80px;'}

        fields = ['longitude', 'latitude', 'altitude']
        widgets = {
            'longitude': forms.TextInput(attrs=common_style),
            'latitude': forms.TextInput(attrs=common_style),
            'altitude': forms.TextInput(attrs=common_style),
        }
