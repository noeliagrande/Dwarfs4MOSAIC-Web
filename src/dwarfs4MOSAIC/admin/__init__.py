"""
Aggregate imports for all model-specific admin modules.
This allows easy and clean import from `admin.py`.
"""

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