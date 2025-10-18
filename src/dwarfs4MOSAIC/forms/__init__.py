"""
This __init__.py file aggregates and exposes the main model classes
from individual modules in the 'forms' package,
allowing easy import of these models directly from 'forms'.
"""

from .form_group import GroupAdminForm
from .form_instrument import InstrumentAdminForm
from .form_observatory import ObservatoryAdminForm
from .form_observing_block import ObservingBlockAdminForm
from .form_observing_run import ObservingRunAdminForm
from .form_researcher import ResearcherAdminForm
from .form_target import TargetAdminForm
from .form_telescope import TelescopeAdminForm

__all__ = ["GroupAdminForm",
           "InstrumentAdminForm",
           "ObservatoryAdminForm",
           "ObservingBlockAdminForm",
           "ObservingRunAdminForm",
           "ResearcherAdminForm",
           "TargetAdminForm",
           "TelescopeAdminForm",
           ]