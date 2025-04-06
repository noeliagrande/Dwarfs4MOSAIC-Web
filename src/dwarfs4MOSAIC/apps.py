from django.apps import AppConfig


class Dwarfs4MOSAICConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dwarfs4MOSAIC'
    verbose_name = "Database"

    def ready(self):
        from . import signals