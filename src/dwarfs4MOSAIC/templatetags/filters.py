# Standard libraries
from math import floor

# Third-party libraries
from django import template
from django.core.exceptions import ValidationError

register = template.Library()

# Registers convert_to_dms function as a filter to be used in templates.
@register.filter
def convert_to_dms(decimal_degree, coord_type='longitude'):
    if decimal_degree is None:
        return ""

    if coord_type == 'longitude':
        # Identify direction (E/W)
        direction = 'E' if decimal_degree >= 0 else 'W'

        # Longitude ranges from -180 to 180
        decimal_degree = abs(decimal_degree)  # Get absolute value for DMS conversion
        if decimal_degree > 180:
            raise ValidationError("Longitude must be in the range [-180, 180].")

    elif coord_type == 'latitude':
        # Identify direction (N/S)
        direction = 'N' if decimal_degree >= 0 else 'S'

        # Latitude ranges from -90 to 90
        decimal_degree = abs(decimal_degree)  # Get absolute value for DMS conversion
        if decimal_degree > 90:
            raise ValidationError("Latitude must be in the range [-90, 90].")

    else:
        raise ValidationError("Invalid coordinate type. Must be 'latitude' or 'longitude'.")

    # Convert decimal value into degrees, minutes and seconds
    degrees = floor(decimal_degree)
    minutes = floor((decimal_degree - degrees) * 60)
    seconds = round(((decimal_degree - degrees) * 60 - minutes) * 60, 2)

    # Format the DMS string
    return f"{degrees}º {minutes}' {seconds}'' {direction}"
