"""
This file contains the Django model that represents an astronomical observatory.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Local application imports
from ..validators import validate_longitude, validate_latitude

class Tbl_observatory(models.Model):

    # Name of the observatory
    name = models.CharField(
        max_length=200,
        verbose_name = "Name")

    # Optional official website URL
    website = models.URLField(
        blank=True,
        verbose_name = "Website",
        default="")

    # Location description (e.g., city or region)
    location = models.CharField(
        max_length=200,
        verbose_name="Location",
        default="")

    # Geographical longitude in deg:min:sec format (string)
    longitude = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Longitude",
        help_text="DD:MM:SS[.sss][E/W]",
        validators=[validate_longitude])


    # Geographical latitude in deg:min:sec format (string)
    latitude = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Latitude",
        help_text="DD:MM:SS[.sss][N/S]",
        validators=[validate_latitude])

    # Altitude of the observatory in meters
    altitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Altitude",
        help_text="meters")

    # Telescopes are linked via a one-to-many relationship defined in Tbl_telescope.
    # Django automatically creates reverse accessors (observatory.tbl_telescope_set).

    def __str__(self):
        # Returns the observatory name when printed or displayed
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Observatory"
        verbose_name_plural = "Observatories"
        ordering = ['name']

