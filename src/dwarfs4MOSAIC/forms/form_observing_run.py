"""
Admin form for observing runs, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..models import Tbl_observing_run

class ObservingRunAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observing_run

        # visual sizes
        area_attrs = {'rows': 3, 'cols': 75}

        fields = ['description', 'comments']
        widgets = {
            'description': forms.Textarea(attrs=area_attrs),
            'comments': forms.Textarea(attrs=area_attrs),
        }
