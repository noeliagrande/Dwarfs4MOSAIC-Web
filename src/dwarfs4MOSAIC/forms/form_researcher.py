"""
Admin form for researchers, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..models import Tbl_researcher

class ResearcherAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_researcher

        # visual sizes
        fields = ['institution', 'comments']
        widgets = {
            'institution': forms.TextInput(attrs={'size': '70'}),
            'comments': forms.Textarea(attrs={'rows': 3, 'cols': 75}),
        }
