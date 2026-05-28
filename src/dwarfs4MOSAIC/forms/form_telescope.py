"""
Admin form for telescopes, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..constants import (
    DROPBOX_OBSERVATORY_WIDTH,
    DROPBOX_WIDTH,
    NAME_WIDTH,
    NUMBER_WIDTH,
    SHORT_DESCRIPTION_WIDTH,
    TEXT_AREA,
    URL_WIDTH,
)

from ..models import Tbl_telescope

class TelescopeAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_telescope

        # visual sizes
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # General Information
            'description'   : forms.TextInput(attrs = {'size': SHORT_DESCRIPTION_WIDTH}),
            'owner'         : forms.Textarea(attrs = TEXT_AREA),
            'obs_tel'       : forms.Select(attrs = {'style': f'width: {DROPBOX_OBSERVATORY_WIDTH}px;'}),
            'status'        : forms.Select(attrs = {'style': f'width: {DROPBOX_WIDTH}px;'}),

            # Characteristics
            'aperture'      : forms.NumberInput(attrs = {'style': f'width: {NUMBER_WIDTH}px;', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adjust width here to preserve Django's default URLField widget behavior
        # without overriding the admin URL widget (current/change/clear links).
        self.fields['website'].widget.attrs.update({'style': f'width: {URL_WIDTH}px;'})