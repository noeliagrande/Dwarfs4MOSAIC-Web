"""
Main admin configuration for the Dwarfs4MOSAIC app.
Sets custom admin site headers and imports all model-specific admin modules.

Aggregate imports for all model-specific admin modules.
This allows easy and clean import from `admin.py`.
"""

# Third-party libraries
from django.contrib import admin

# Set custom header and title for the admin site
admin.site.site_header = "Dwarfs4MOSAIC Administration" # default: "Django administration"
admin.site.site_title = "Dwarfs4MOSAIC Admin Portal"
admin.site.index_title = "dwarfs4MOSAIC Administration" # default: "Site administration"

from . import admin_group
from . import admin_instrument
from . import admin_observatory
from . import admin_observing_block
from . import admin_observing_run
from . import admin_researcher
from . import admin_target
from . import admin_telescope
from . import admin_user


__all__ = ["admin_group",
           "admin_instrument",
           "admin_observatory",
           "admin_observing_block",
           "admin_observing_run",
           "admin_researcher",
           "admin_target",
           "admin_telescope",
           "admin_user",
           ]