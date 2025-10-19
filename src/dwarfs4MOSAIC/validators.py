"""
Astronomical coordinate validators for Django models.

This module provides functions to validate standard astronomical
coordinates commonly used in observations and catalogs. The
validators ensure that the input strings follow the correct
format and represent physically meaningful values.

"""

# Standard libraries
import re

# Local application imports
from django.core.exceptions import ValidationError

# Regular expression to validate Longitude (LON).
def validate_longitude(value):

    if not value:
        return  # empty field

    # Format DDD:MM:SS[.sss][E/W].
    # ^                                     -> start of string
    # (?:[0-9]{1,2}|[0-1][0-7][0-9]|180)    -> degrees, 0-180
    # :[0-5][0-9]                           -> minutes, 00-59
    # :[0-5][0-9]                           -> seconds, 00-59
    # (?:\.\d+)?                            -> Optional decimal part for fractional seconds
    # [EW]                                  -> hemisphere, E or W
    # $                                     -> end of string
    pattern = r'^(?:[0-9]{1,2}|[0-1][0-7][0-9]|180):[0-5][0-9]:[0-5][0-9](?:\.\d+)?[EW]$'

    if not re.match(pattern, value):
        raise ValidationError('Invalid format.')

    # Absolute value <= 180 degrees

    # Split into degrees, minutes, seconds, hemisphere
    degrees, minutes, sec_hem = value.split(':')
    seconds = sec_hem[:-1]
    hem = sec_hem[-1]

    degrees = int(degrees)
    minutes = int(minutes)
    seconds = float(seconds)

    decimal_deg = degrees + minutes / 60 + seconds / 3600
    if hem == 'W':
        decimal_deg *= -1

    if not -180 <= decimal_deg <= 180:
        raise ValidationError('Longitude must be between -180 and 180 degrees.')


# Regular expression to validate Latitude (LAT).
def validate_latitude(value):

    if not value:
        return  # empty field

    # Format DD:MM:SS[.sss][N/S].
    # ^                     -> start of string
    # (?:[0-8][0-9]|90)    -> degrees, 0-90
    # :[0-5][0-9]           -> minutes, 00-59
    # :[0-5][0-9]           -> seconds, 00-59
    # (?:\.\d+)?            -> Optional decimal part for fractional seconds
    # [NS]                  -> hemisphere, N or S
    # $                     -> end of string
    pattern = r'^(?:[0-8][0-9]|90):[0-5][0-9]:[0-5][0-9](?:\.\d+)?[NS]$'

    if not re.match(pattern, value):
        raise ValidationError('Invalid format.')

    # Absolute value <= 90 degrees

    # Split into degrees, minutes, seconds, hemisphere
    degrees, minutes, sec_hem = value.split(':')
    seconds = sec_hem[:-1]
    hem = sec_hem[-1]

    degrees = int(degrees)
    minutes = int(minutes)
    seconds = float(seconds)

    decimal_deg = degrees + minutes / 60 + seconds / 3600
    if hem == 'S':
        decimal_deg *= -1

    if not -90 <= decimal_deg <= 90:
        raise ValidationError('Latitude must be between -90 and 90 degrees.')

# Regular expression to validate Right Ascension (RA).
def validate_right_ascension(value):

    if not value:
        return  # empty field

    # Format HH:MM:SS[.sss]:
    # ^                    -> Start of the string
    # (?:[01][0-9]|2[0-3]) -> Hours: either 00–19 ([01][0-9]) or 20–23 (2[0-3])
    # :[0-5][0-9]          -> Minutes: two digits from 00 to 59
    # :[0-5][0-9]          -> Seconds: two digits from 00 to 59
    # (?:\.\d+)?           -> Optional decimal part for fractional seconds
    # $                    -> End of the string
    pattern = r'^(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.\d+)?$'

    if not re.match(pattern, value):
        raise ValidationError('Invalid format.')

# Regular expression to validate Declination (DEC).
def validate_declination(value):
    if not value:
        return  # empty field

    # Format ±DD:MM:SS[.sss]:
    # ^                     -> Start of the string
    # [+-]                  -> Must start with + or - sign
    # (?:[0-8][0-9]|90)     -> Degrees: 00-89 or exactly 90
    # :[0-5][0-9]           -> Minutes: 00-59
    # :[0-5][0-9]           -> Seconds: 00-59
    # (?:\.\d+)?            -> Optional fractional seconds
    # $                     -> End of the string
    pattern = r'^[+-](?:[0-8][0-9]|90):[0-5][0-9]:[0-5][0-9](?:\.\d+)?$'

    if not re.match(pattern, value):
        raise ValidationError('Invalid format.')

    # Absolute value <= 90 degrees

    # Split into sign, degrees, minutes, seconds
    sign = 1 if value[0] == '+' else -1
    degrees, minutes, seconds = value[1:].split(':')
    degrees = int(degrees)
    minutes = int(minutes)
    seconds = float(seconds)

    # Compute total declination in degrees
    total_deg = sign * (degrees + minutes / 60 + seconds / 3600)

    if not -90 <= total_deg <= 90:
        raise ValidationError('Declination must be between -90 and 90 degrees.')