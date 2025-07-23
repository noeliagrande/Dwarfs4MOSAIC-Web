"""
This file defines how Group admin model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

# Local application imports
from ..forms import GroupAdminForm

# Replace default Group admin with custom form and fieldsets
admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(DefaultGroupAdmin):

    # Custom form with file upload fields
    form = GroupAdminForm

    # Group fields into sections in the admin form
    def get_fieldsets(self, request, obj=None):
        base_fieldsets = [
            (None, {'fields': ('name', 'permissions')})
        ]

        # When editing existing Group, add authorization section
        if obj and obj.pk:
            base_fieldsets.append(
                ('Authorization', {'fields': ('allowed_blocks',)})
            )

        return base_fieldsets


    def save_model(self, request, obj, form, change):
        # Detect if the object is new (being created)
        is_new = obj.pk is None

        # Save the model normally first
        super().save_model(request, obj, form, change)

        if is_new:
            return

    # Override response after adding object: redirect to change page,
    # except when using "Save and add another" (then redirect to add new)
    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" in request.POST:
            # Default behaviour for 'Save and add another' (go to add new)
            return super().response_add(request, obj, post_url_continue)
        elif "_continue" in request.POST or "_save" in request.POST:
            # For both 'Save and continue editing' and 'Save',
            # redirect to the change page of the newly created object
            url = self.get_change_url(obj)
            return HttpResponseRedirect(url)
        else:
            return super().response_add(request, obj, post_url_continue)

    # Build URL for change page of this object in admin
    def get_change_url(self, obj):
        opts = self.model._meta
        return f"/admin/{opts.app_label}/{opts.model_name}/{obj.pk}/change/"