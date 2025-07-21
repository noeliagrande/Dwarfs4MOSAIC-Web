"""
ASGI config for website project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# Standard libraries
import os

# Third-party libraries
from django.core.asgi import get_asgi_application

# Set the default settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dwarfs4MOSAIC_website.settings')

# Create the ASGI application instance for handling requests
application = get_asgi_application()
