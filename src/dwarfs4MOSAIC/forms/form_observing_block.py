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

        fields = ['semester', 'exposure_time', 'seeing']
        widgets = {
            'semester': forms.TextInput(attrs=common_style),
            'exposure_time': forms.TextInput(attrs = common_style),
            'seeing': forms.NumberInput(attrs=common_style),
        }
