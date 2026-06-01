"""
Context processor for injecting the app version into templates.

This allows you to access the `APP_VERSION` setting from any template using {{ APP_VERSION }}.
"""

# Local application imports
from .version import __version__ as APP_VERSION

# Context processor to add the application version to all templates
def app_version(request):
    return {'APP_VERSION': APP_VERSION}
