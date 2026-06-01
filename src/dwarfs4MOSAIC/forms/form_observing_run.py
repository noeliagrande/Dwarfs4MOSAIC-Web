"""
Admin form for observing runs, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..admin.helpers import set_related_view_only
from ..constants import (
    DROPBOX_WIDTH,
    NAME_WIDTH,
    TEXT_AREA,
)
from ..models import Tbl_observing_run

class ObservingRunAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observing_run

        # visual sizes
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # General Information
            'description'   : forms.Textarea(attrs = TEXT_AREA),
            'instrument'    : forms.Select(attrs={'style': f'width: {DROPBOX_WIDTH}px;'}),

            # Additional Data
            'comments': forms.Textarea(attrs = TEXT_AREA),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict related field widget to view-only mode
        # (disable add/edit/delete links in admin form)
        set_related_view_only(self.fields["instrument"])