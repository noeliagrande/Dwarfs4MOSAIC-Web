"""
App configuration for the dwarfs4MOSAIC Django application.

This class defines the app settings such as the default primary key field type,
app name, and the human-readable name shown in the Django admin interface.
It also imports signal handlers when the app is fully loaded.
"""

from django.apps import AppConfig

class Dwarfs4MOSAICConfig(AppConfig):
    # Default primary key type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Internal name of the Django app
    name = 'dwarfs4MOSAIC'

    # Display name of the app in the Django admin
    verbose_name = "Database"

    def ready(self):
        # Import signal handlers to connect signals with their receivers
        from . import signals