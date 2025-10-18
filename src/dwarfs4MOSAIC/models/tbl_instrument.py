"""
This file contains the Django model that represents an instrument installed on a telescope.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.db import models

# Local application imports
from .tbl_telescope import Tbl_telescope

class Tbl_instrument(models.Model):

    # Name of the instrument
    name = models.CharField(
        max_length=200,
        verbose_name = "Name")

    # Optional short description of the instrument
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Description")

    # Telescope where the instrument is installed (foreign key to Tbl_telescope)
    tel_ins = models.ForeignKey(
        Tbl_telescope,
        on_delete=models.PROTECT,
        null=True,
        verbose_name = "Telescope")

    # Current operational status of the instrument
    status = models.CharField(
        choices=[
            ('unknown', 'Unknown'),
            ('operational', 'Operational'),
            ('inoperative', 'Inoperative'),
            ('maintenance', 'Under Maintenance')],
        max_length=11,  # must be long enough to hold the longest choice
        default='unknown',
        verbose_name="Status")

    # Optional website URL with more information about the instrument
    website = models.URLField(
        verbose_name="Website",
        blank=True,
        default="")

    # List of filters, stored as comma-separated string
    filters = models.TextField(
        blank=True,
        help_text="Comma-separated"
    )

    # List of configurations, stored as comma-separated string
    configuration = models.TextField(
        verbose_name="Configurations",
        blank=True,
        help_text="Comma-separated"
    )

    @property
    def filters_list(self):
        """Return filters as a Python list of strings."""
        return [f.strip() for f in self.filters.split(',') if f.strip()]

    @property
    def configuration_list(self):
        """Return configurations as a Python list of strings."""
        return [c.strip() for c in self.configuration.split(',') if c.strip()]

    def __str__(self):
        # Returns the instrument name when printed or displayed
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['name']

