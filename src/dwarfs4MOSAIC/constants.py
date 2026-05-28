"""
Application-wide constants used across Django models, forms, and admin UI.

This module centralizes:
    - Database-related constraints (e.g. max lengths for model fields)
    - Form and Django admin visual settings (e.g. widget widths and text areas)

Keeping these values in a single place improves consistency and simplifies future maintenance and UI adjustments.
"""

# MODEL (database constraints)
# ----------------------------

# Maximum string lengths used in model fields
COORDINATE_MAX_LENGTH           = 15
NAME_MAX_LENGTH                 = 100
SHORT_DESCRIPTION_MAX_LENGTH    = 255
STATUS_MAX_LENGTH               = 20


# UI CONSTANTS (forms / Django admin display)
# -------------------------------------------

# Input widths

# Text-based widgets use character units
COORDINATE_WIDTH            = 15
NAME_WIDTH                  = 40
SHORT_DESCRIPTION_WIDTH     = 75
URL_WIDTH                   = 1000


# Numeric and select widgets use pixels
DROPBOX_WIDTH               = 200
DROPBOX_OBSERVATORY_WIDTH   = 250
NUMBER_WIDTH                = 125
REDSHIFT_WIDTH              = 125

# Text areas
CONFIG_AREA     = {'rows': 3, 'cols': 30}
FILTERS_AREA    = {'rows': 3, 'cols': 30}
INFO_AREA       = {'rows': 20, 'cols': 100}
TEXT_AREA       = {'rows': 5, 'cols': 100}



