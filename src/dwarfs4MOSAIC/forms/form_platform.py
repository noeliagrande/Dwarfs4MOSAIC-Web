"""
Admin form for platform info, to set control size.
"""

# Third-party libraries
from django import forms

class PlatformInfoForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}),
        label='Platform Information'
    )
