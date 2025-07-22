"""
Main admin configuration for the Dwarfs4MOSAIC app.
Sets custom admin site headers and imports all model-specific admin modules.
"""

# Third-party libraries
from django.contrib import admin

# Set custom header and title for the admin site
admin.site.site_header = "Dwarfs4MOSAIC Administration" # default: Django administration
admin.site.site_title = "Dwarfs4MOSAIC Admin Portal"
# admin.site.index_title = "Site administration" (default)

from admin import *