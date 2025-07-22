"""
Admin form for groups with custom allowed blocks field
"""

# Third-party libraries
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group


# Local application imports
from ..models import Tbl_observing_block

# Admin form for groups with custom allowed blocks field
class GroupAdminForm(forms.ModelForm):
    allowed_blocks = forms.ModelMultipleChoiceField(
        queryset=Tbl_observing_block.objects.all(),
        required=False,
        label = '',
        widget=admin.widgets.FilteredSelectMultiple("Observing Blocks", is_stacked=False)
    )

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Use detailed name for allowed blocks in the selection list
        self.fields['allowed_blocks'].label_from_instance = lambda obj: obj.detailed_name

        # Set initial allowed blocks if the group already exists
        if self.instance.pk:
            self.fields['allowed_blocks'].initial = self.instance.allowed_blocks.all()

    def save(self, commit=True):
        # Save group and update allowed blocks relation
        group = super().save(commit=False)
        if commit:
            group.save()
        if group.pk:
            group.allowed_blocks.set(self.cleaned_data['allowed_blocks'])
            self.save_m2m()
        return group