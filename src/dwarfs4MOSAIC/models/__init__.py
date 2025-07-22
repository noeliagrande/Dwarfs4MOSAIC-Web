"""
This __init__.py file aggregates and exposes the main model classes
from individual modules in the 'models' package,
allowing easy import of these models directly from 'models'.
"""

from .tbl_instrument import Tbl_instrument
from .tbl_observatory import Tbl_observatory
from .tbl_observing_block import Tbl_observing_block
from .tbl_observing_run import Tbl_observing_run
from .tbl_researcher import Tbl_researcher
from .tbl_target import Tbl_target
from .tbl_telescope import Tbl_telescope

__all__ = ["Tbl_instrument",
           "Tbl_observatory",
           "Tbl_observing_block",
           "Tbl_observing_run",
           "Tbl_researcher",
           "Tbl_target",
           "Tbl_telescope",
           ]