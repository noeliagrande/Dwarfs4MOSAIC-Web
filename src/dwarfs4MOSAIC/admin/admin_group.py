"""
This file defines how Group admin model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from django.contrib.auth.models import Group


# Local application imports
from ..forms import GroupAdminForm

# Replace default Group admin with custom form and fieldsets
admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(DefaultGroupAdmin):
    form = GroupAdminForm

    # Define fields and additional authorization fields
    fieldsets = (
        (None, {'fields': ('name', 'permissions')}),
        ('Authorization', {'fields': ('allowed_blocks',)}),
    )

