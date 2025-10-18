"""
Admin form for observing blocks, to set control size.
"""

# Standard libraries
import os

# Third-party libraries
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe

# Local application imports
from ..models import Tbl_observing_block
from ..utils import SingleFileField, MultipleFileField


# Admin form for observing blocks
class ObservingBlockAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observing_block

        # visual sizes
        common_style = {'style': 'width:80px;'}

        fields = ['semester', 'filters', 'configuration', 'exposure_time', 'seeing']
        widgets = {
            'semester': forms.TextInput(attrs=common_style),
            'filters': forms.Select(attrs={'style': 'width:120px;', 'class': 'dynamic-select'}),
            'configuration': forms.Select(attrs={'style': 'width:120px;', 'class': 'dynamic-select'}),
            'exposure_time': forms.TextInput(attrs = common_style),
            'seeing': forms.NumberInput(attrs=common_style),
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
            choices=filter_choices,
            attrs={'style': 'width:120px;'}
        )
        self.fields['configuration'].widget = forms.Select(
            choices=config_choices,
            attrs={'style': 'width:120px;'}
        )

    class Media:
        js = ('js/observing_block.js',)