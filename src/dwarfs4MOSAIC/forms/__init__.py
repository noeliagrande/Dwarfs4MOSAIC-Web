"""
This __init__.py file aggregates and exposes the main model classes
from individual modules in the 'forms' package,
allowing easy import of these models directly from 'forms'.
"""

from .form_group import GroupAdminForm
from .form_observatory import ObservatoryAdminForm
from .form_instrument import InstrumentAdminForm
from .form_target import TargetAdminForm

__all__ = ["GroupAdminForm",
           "ObservatoryAdminForm",
           "InstrumentAdminForm",
           "TargetAdminForm",
           ]