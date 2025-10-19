
# Standard libraries
import re

# Local application imports
from django.core.exceptions import ValidationError

# Regular expression to validate Right Ascension (RA).
def validate_right_ascension(value):

    if not value:
        return  # empty field

    # Format HH:MM:SS[.sss]:
    # ^                    → Start of the string
    # (?:[01][0-9]|2[0-3]) → Hours: either 00–19 ([01][0-9]) or 20–23 (2[0-3])
    # :                    → Literal colon separating hours and minutes
    # [0-5][0-9]           → Minutes: two digits from 00 to 59
    # :                    → Literal colon separating minutes and seconds
    # [0-5][0-9]           → Seconds: two digits from 00 to 59
    # (?:\.\d+)?           → Optional decimal part for fractional seconds (e.g., .5, .123)
    # $                    → End of the string
    pattern = r'^(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.\d+)?$'

    if not re.match(pattern, value):
        raise ValidationError(f'{value} is not a valid value.')

# Regular expression to validate Declination (DEC).
def validate_declination(value):
    if not value:
        return  # empty field

    # Format ±DD:MM:SS[.sss]:
    # ^[+-]                 -> Must start with + or - sign
    # (?:[0-8][0-9]|90)     -> Degrees: 00-89 or exactly 90
    # :[0-5][0-9]           -> Minutes: 00-59
    # :[0-5][0-9]           -> Seconds: 00-59
    # (?:\.\d+)?$           -> Optional fractional seconds (e.g., 12.345)
    pattern = r'^[+-](?:[0-8][0-9]|90):[0-5][0-9]:[0-5][0-9](?:\.\d+)?$'

    if not re.match(pattern, value):
        raise ValidationError(f'{value} is not a valid value.')

    # Absolute value <= 90 degrees

    # Split into sign, degrees, minutes, seconds
    sign = 1 if value[0] == '+' else -1
    deg, minute, second = value[1:].split(':')
    deg = int(deg)
    minute = int(minute)
    second = float(second)

    # Compute total declination in degrees
    total_deg = sign * (deg + minute / 60 + second / 3600)

    if not -90 <= total_deg <= 90:
        raise ValidationError(f'{value} exceeds limits (-90 to +90).')