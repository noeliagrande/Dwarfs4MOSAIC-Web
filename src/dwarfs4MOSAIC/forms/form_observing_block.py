"""
Admin form for observing blocks, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..admin.helpers import set_related_view_only
from ..constants import (
    DROPBOX_WIDTH,
    NAME_WIDTH,
    NUMBER_WIDTH,
    TEXT_AREA,
)
from ..models import Tbl_observing_block

class ObservingBlockAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observing_block

        # visual sizes
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # General Information
            'obs_run'       : forms.Select(attrs = {'style': f'width: {DROPBOX_WIDTH}px;'}),
            'description'   : forms.Textarea(attrs = TEXT_AREA),
            'semester'      : forms.TextInput(attrs = {'size': NAME_WIDTH}),

            # Observation Information
            'observation_mode'  : forms.Select(attrs = {'style': f'width: {DROPBOX_WIDTH}px;'}),
            'filters'           : forms.Select(attrs = {'class': 'dynamic-select'}),
            'configuration'     : forms.Select(attrs = {'class': 'dynamic-select'}),
            'exposure_time'     : forms.NumberInput(attrs = {'style': f'width: {NUMBER_WIDTH}px;', 'min': '0'}),
            'seeing'            : forms.NumberInput(attrs = {'style': f'width: {NUMBER_WIDTH}px;', 'min': '0'}),
            'weather_conditions': forms.Textarea(attrs = TEXT_AREA),
            'comments'          : forms.Textarea(attrs = TEXT_AREA),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Associated instrument
        obs_run = getattr(self.instance, 'obs_run', None)
        instrument = getattr(obs_run, 'instrument', None)

        # Initialize empty choices
        filter_choices = [('', '---------')]
        config_choices = [('', '---------')]

        if instrument:
            filter_choices += [(f, f) for f in instrument.filters_list]
            config_choices += [(c, c) for c in instrument.configuration_list]

        # Replace text widgets with Select
        self.fields['filters'].widget = forms.Select(
            choices = filter_choices,
            attrs   = {'style': f'width: {DROPBOX_WIDTH}px;'}
        )
        self.fields['configuration'].widget = forms.Select(
            choices = config_choices,
            attrs   = {'style': f'width: {DROPBOX_WIDTH}px;'}
        )

        # Restrict related field widget to view-only mode
        # (disable add/edit/delete links in admin form)
        set_related_view_only(self.fields["obs_run"])

    class Media:
        js = ('js/observing_block.js',)