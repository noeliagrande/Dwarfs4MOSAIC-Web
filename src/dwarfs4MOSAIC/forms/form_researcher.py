"""
Admin form for researchers, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..constants import (
    DROPBOX_WIDTH,
    SHORT_DESCRIPTION_WIDTH,
    TEXT_AREA,
)
from ..models import Tbl_researcher

class ResearcherAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_researcher

        # visual sizes
        fields = "__all__"
        widgets = {
            'role': forms.Select(attrs={'style': f'width: {DROPBOX_WIDTH}px;'}),

            # General Information
            'institution'   : forms.TextInput(attrs = {'size': SHORT_DESCRIPTION_WIDTH}),
            'comments'      : forms.Textarea(attrs = TEXT_AREA),
        }
