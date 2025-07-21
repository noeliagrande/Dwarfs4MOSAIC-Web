"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# Standard libraries
import os

# Third-party libraries
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dwarfs4MOSAIC_website.settings')

# Create the WSGI application instance for serving the project
application = get_wsgi_application()
