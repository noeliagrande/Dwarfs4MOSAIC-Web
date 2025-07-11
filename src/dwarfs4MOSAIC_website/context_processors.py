"""
Context processor for injecting the app version into templates.

This allows you to access the `APP_VERSION` setting from any template using {{ APP_VERSION }}.
"""

from django.conf import settings

def app_version(request):
    return {'APP_VERSION': settings.APP_VERSION}
