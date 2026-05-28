"""
Admin form for instruments, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..constants import (
    CONFIG_AREA,
    DROPBOX_WIDTH,
    FILTERS_AREA,
    NAME_WIDTH,
    SHORT_DESCRIPTION_WIDTH,
    URL_WIDTH,
)
from ..models import Tbl_instrument

class InstrumentAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_instrument

        # visual sizes
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # General Information
            'description'   : forms.TextInput(attrs = {'size': SHORT_DESCRIPTION_WIDTH}),
            'tel_ins'       : forms.Select(attrs = {'style': f'width: {DROPBOX_WIDTH}px;'}),
            'status'        : forms.Select(attrs = {'style': f'width: {DROPBOX_WIDTH}px;'}),

            # Additional Data
            'filters'       : forms.Textarea(attrs = FILTERS_AREA),
            'configuration' : forms.Textarea(attrs = CONFIG_AREA),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adjust width here to preserve Django's default URLField widget behavior
        # without overriding the admin URL widget (current/change/clear links).
        self.fields['website'].widget.attrs.update({'style': f'width: {URL_WIDTH}px;'})