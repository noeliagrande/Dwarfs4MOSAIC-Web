"""
Admin form for observatories with detailed longitude and latitude input fields.
Longitude and latitude are split into direction (E/W, N/S), degrees, minutes, and seconds.
Includes conversion between decimal degrees and DMS, and validation of input completeness and range.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..constants import (
    COORDINATE_WIDTH,
    NAME_WIDTH,
    URL_WIDTH,
)
from ..models import Tbl_observatory

class ObservatoryAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observatory

        # visual sizes
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # General Information
            'location': forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # Coordinates
            'longitude' : forms.TextInput(attrs = {'size': COORDINATE_WIDTH}),
            'latitude'  : forms.TextInput(attrs = {'size': COORDINATE_WIDTH}),
            'altitude'  : forms.TextInput(attrs = {'size': COORDINATE_WIDTH}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adjust width here to preserve Django's default URLField widget behavior
        # without overriding the admin URL widget (current/change/clear links).
        self.fields['website'].widget.attrs.update({'style': f'width: {URL_WIDTH}px;'})
