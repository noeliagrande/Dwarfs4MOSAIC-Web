"""
This file contains the Django model that represents an observing run,
a scheduled period of observations using a specific instrument.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.db import models

# Local application imports
from ..models import Tbl_instrument

class Tbl_observing_run(models.Model):

    # Name of the observing run
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    # Optional description of the observing run
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description")

    # Instrument used during the observing run (foreign key to Tbl_instrument)
    instrument = models.ForeignKey(
        Tbl_instrument,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Instrument")

    # Start date of the observing run
    start_date = models.DateField(
        verbose_name="Start Date")

    # Optional end date of the observing run
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="End Date")

    # Researchers participating in the observing run (many-to-many relationship)
    researchers = models.ManyToManyField(
        'Tbl_researcher',
        blank=True,
        related_name='observing_runs'
    )

    # Additional notes or comments about the observing run
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    def __str__(self):
        # Returns the observing run name when printed or displayed
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Observing Run"
        verbose_name_plural = "Observing Runs"
        ordering = ['start_date']
