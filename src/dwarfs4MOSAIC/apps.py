"""
App configuration for the dwarfs4MOSAIC Django application.

This class defines the app settings such as the default primary key field type,
app name, and the human-readable name shown in the Django admin interface.
It also imports signal handlers when the app is fully loaded.
"""

# Third-party libraries
from django.apps import AppConfig

# Configuration class for the dwarfs4MOSAIC app
class Dwarfs4MOSAICConfig(AppConfig):
    # Default type for auto-generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'

    # Internal name of the app
    name = 'dwarfs4MOSAIC'

    # Name displayed in the Django admin
    verbose_name = "Database"

    def ready(self):
        # Import signals to connect model events to handlers
        from . import signals