"""
Admin form for observing blocks, to set control size.
"""

# Third-party libraries
from django import forms

# Local application imports
from ..models import Tbl_observing_block

class ObservingBlockAdminForm(forms.ModelForm):

    class Meta:
        model = Tbl_observing_block

        # visual sizes
        text_attrs = {'style': 'width:80px;'}
        area_attrs = {'rows': 3, 'cols': 75}

        fields = ['description', 'semester', 'filters', 'configuration',
                  'exposure_time', 'seeing', 'weather_conditions', 'comments']
        widgets = {
            'description': forms.Textarea(attrs=area_attrs),
            'semester': forms.TextInput(attrs=text_attrs),
            'filters': forms.Select(attrs={'style': 'width:120px;', 'class': 'dynamic-select'}),
            'configuration': forms.Select(attrs={'style': 'width:120px;', 'class': 'dynamic-select'}),
            'exposure_time': forms.TextInput(attrs = text_attrs),
            'seeing': forms.NumberInput(attrs=text_attrs),
            'weather_conditions': forms.Textarea(attrs=area_attrs),
            'comments': forms.Textarea(attrs=area_attrs),
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