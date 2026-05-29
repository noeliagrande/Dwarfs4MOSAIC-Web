"""
This file defines how Tbl_researcher model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.urls import reverse

# Local application imports
from ..forms import ResearcherAdminForm
from ..models import Tbl_researcher


# Admin interface for Tbl_researcher with enhanced UI
@admin.register(Tbl_researcher)
class ResearcherAdmin(admin.ModelAdmin):

    # Display main identifying fields for quick overview
    list_display = ("name", "institution", "role", "is_phd", "email")

    # Default ordering in changelist (case-insensitive + fallback)
    ordering = (Lower("name"),"name")

    # Custom ModelForm for validation and layout control
    form = ResearcherAdminForm

    # Group fields into logical sections for better usability
    fieldsets = [
        (None, {"fields": ['user', 'role']}),
        ("General Information", {"fields": [
            'is_phd', 'institution', 'comments']}),
        ("Authorization", {"fields": [
            "denied_blocks"]}),
    ]

    # Multi-select widget for denied_blocks
    filter_horizontal = ['denied_blocks']

    # Redirect creation of a Researcher to the Django User creation page
    def add_view(self, request, form_url='', extra_context=None):
        user_admin_url = reverse('admin:auth_user_add')
        return redirect(user_admin_url)

    # Always show user field, just make it readonly when editing.
    def get_fieldsets(self, request, obj=None):
        return self.fieldsets

    # Control field editability depending on whether the object is linked to a User
    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.user is None:
            # If no linked user, make all fields read-only
            return [f.name for f in self.model._meta.fields] + ['denied_blocks']
        if obj:
            # When editing with linked user, make only 'user' read-only
            return ['user']
        return super().get_readonly_fields(request, obj)

    # Hide save buttons when researcher is not linked to a user account
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Hide save buttons if researcher has no linked user
        extra_context = extra_context or {}
        if object_id:
            researcher = Tbl_researcher.objects.get(pk=object_id)
            if researcher.user is None:
                extra_context['show_save'] = False
                extra_context['show_save_and_add_another'] = False
                extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

