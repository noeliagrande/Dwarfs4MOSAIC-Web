"""
This file defines how User admin model is displayed and managed in the Django Admin interface.
"""

# Third-party libraries
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse

# Local application imports
from ..models import Tbl_researcher


# Custom User admin to add link to linked Researcher if exists
class CustomUserAdmin(DefaultUserAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        user = User.objects.filter(pk=object_id).first()
        extra_context = extra_context or {}

        # Add link to Researcher admin page if user has linked researcher
        try:
            researcher = user.researcher
            researcher_url = reverse(
                'admin:dwarfs4MOSAIC_tbl_researcher_change',
                args=[researcher.pk]
            )
            extra_context['researcher_link'] = researcher_url
        except Tbl_researcher.DoesNotExist:
            extra_context['researcher_link'] = None

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

# Replace default User admin with custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

