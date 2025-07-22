"""
This file contains the Django model that represents a telescope located at an observatory.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.core.validators import MinValueValidator
from django.db import models

# Local application imports
from .tbl_observatory import Tbl_observatory

class Tbl_telescope(models.Model):

    # Name of the telescope
    name = models.CharField(
        max_length=200,
        verbose_name = "Name")

    # Optional short description of the telescope
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Description")

    # Observatory where the telescope is located (foreign key to Tbl_observatory)
    obs_tel = models.ForeignKey(
        Tbl_observatory,
        on_delete=models.PROTECT,
        null=True,
        verbose_name = "Observatory")

    # Institutional owner of the telescope
    owner = models.TextField(
        default="",
        verbose_name = "Institutional Owner")

    # Aperture size in meters (must be >= 0)
    aperture = models.FloatField(
        verbose_name="Aperture",
        default=0,
        validators=[MinValueValidator(0)],
        help_text="meters")

    # Current operational status of the telescope
    status = models.CharField(
        choices=[
            ('unknown', 'Unknown'),
            ('operational', 'Operational'),
            ('inoperative', 'Inoperative'),
            ('maintenance', 'Under Maintenance')],
        max_length=11, # must be long enough to hold the longest choice
        default='unknown',
        verbose_name="Status")

    # Optional website URL with more information about the telescope
    website = models.URLField(
        verbose_name="Website",
        blank=True,
        null=True,
        default="")

    # Instruments are linked via a one-to-many relationship defined in Tbl_instrument.
    # Django automatically creates reverse accessors (telescope.tbl_instrument_set).

    def __str__(self):
        # Returns the telescope name when printed or displayed
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Telescope"
        verbose_name_plural = "Telescopes"
        ordering = ['name']

