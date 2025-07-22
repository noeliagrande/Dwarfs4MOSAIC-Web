"""
This file contains the Django model that represents an astronomical observatory.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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

    # Geographical longitude in degrees (-180 to 180)
    longitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)])

    # Geographical latitude in degrees (-90 to 90)
    latitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)])

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

