"""
This file contains the Django model that represents an observing block,
a specific set of observations scheduled within an observing run.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.contrib.auth.models import Group
from django.db import models

# Local application imports
from .tbl_observing_run import Tbl_observing_run

class Tbl_observing_block(models.Model):

    # Name of the observing block
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    # Observing run where this block is executed (foreign key to Tbl_observing_run)
    obs_run = models.ForeignKey(
        Tbl_observing_run,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Observing Run")

    # Optional description of the observing block
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description")

    # Start date and time of the block
    start_time = models.DateTimeField(
        verbose_name="Start Time")
        
    # Optional end time (time only, no date) of the block
    end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="End Time")

    # Targets observed in this block (many-to-many relationship)
    target = models.ManyToManyField(
        'Tbl_target',
        blank=True,
        related_name='observing_blocks'
    )

    # Observation mode used during the block
    observation_mode = models.CharField(
        choices=[
            ('photometry', 'Photometry'),
            ('spectroscopy', 'Spectroscopy'),
            ('imaging', 'Imaging')],
        max_length=12,  # maximum length in choices
        default='photometry',
        verbose_name="Observation Mode")

    # Filters used during the observations
    filters = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Filters")

    # Exposure time per observation (in seconds)
    exposure_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Exposure Time",
        help_text="seconds")
        
    # Seeing value during the observation (in arcseconds)
    seeing = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Seeing",
        help_text="arcsec")
        
    # Weather conditions during the observing block
    weather_conditions = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Weather Conditions")
    
    # Additional notes or comments about the observing block
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    # Groups that have access to this observing block
    allowed_groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="allowed_blocks",
        help_text="Groups that have access to this observing block"
    )

    @property
    def detailed_name(self):
        """
        Returns a detailed description combining:
        - Block name
        - Associated instrument (if available)
        - Observation date (if available)
        """

        # Observing_block name
        name = self.name

        # Instrument (may not exist)
        if self.obs_run and self.obs_run.instrument:
            instrument = self.obs_run.instrument.name
        else:
            instrument = "No instrument"

        # Observation date (may not exist)
        if self.start_time:
            obs_date = self.start_time.strftime('%Y-%m-%d')
        else:
            obs_date = "No date"

        return f"{name} - {instrument} ({obs_date})"

    def __str__(self):
        # Returns the block name when printed or displayed
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Observing Block"
        verbose_name_plural = "Observing Blocks"
        ordering = ['start_time']
