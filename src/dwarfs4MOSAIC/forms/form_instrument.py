"""
Admin form for instruments, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..models import Tbl_instrument

class InstrumentAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_instrument

        # visual sizes
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={'size': '75'}),
        }

