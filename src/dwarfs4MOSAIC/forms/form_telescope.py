"""
Admin form for telescopes, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..models import Tbl_telescope

class TelescopeAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_telescope

        # visual sizes
        fields = ['owner', 'aperture']
        widgets = {
            'owner': forms.Textarea(attrs={'rows': 3, 'cols': 75}),
            'aperture': forms.NumberInput(attrs={'style': 'width:80px;', 'min': '0'}),
        }
