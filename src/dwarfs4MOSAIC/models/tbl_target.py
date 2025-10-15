"""
This file contains the Django model that represents an astronomical target,
such as a galaxy, calibration source, or other object.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Standard libraries
import os
import shutil

# Third-party libraries
from django.conf import settings
from django.db import models

# Local application imports
from ..utils import sanitize_filename

class Tbl_target(models.Model):

    # Unique target name
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Name")

    # Target type with predefined choices
    type = models.CharField(
        choices=[
            ('galaxy', 'Galaxy'),
            ('calibration', 'Calibration'),
            ('other', 'Other'), ],
        max_length=20,  # maximum length in choices
        default='galaxy',
        verbose_name="Type")

    # Right Ascension in HH:MM:SS format (string)
    right_ascension = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Right Ascension",
        help_text="HH:MM:SS")

    # Declination in +/- degrees:minutes:seconds format (string)
    declination = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Declination",
        help_text="+/- deg:min:sec")

    # Apparent magnitude (Vega system)
    magnitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Magnitude",
        help_text="Referenced to Vega System")

    # Redshift of the target
    redshift = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Redshift (z)")

    # Angular size of the object in arcseconds
    size = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Size",
        help_text="arcsec",)

    # Semester in which the target is visible
    semester = models.CharField(
        max_length=10,
        verbose_name="Visibility semester")

    # Optional comments or notes about the target
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    # Relative path to the image file under MEDIA_ROOT (not editable in admin)
    image = models.CharField( # Image relative path to MEDIA_ROOT
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Image",
        editable=False,
    )

    # Relative path to associated data files under MEDIA_ROOT (not editable in admin)
    datafiles_path = models.CharField( # Data files relative path to MEDIA_ROOT
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Data files path",
        editable=False,
    )

    @property
    def image_name(self):
        """
        Returns the basename of the image file if the image path and extension exist,
        otherwise returns an empty string.
        """
        if self.image and os.path.splitext(self.image)[1]:  # if file extension exists
            return os.path.basename(self.image)
        return ""

    def __init__(self, *args, **kwargs):
        """
        If the stored target type is no longer valid (not in choices),
        set it to 'other' for display, but preserve original in DB.
        """
        super().__init__(*args, **kwargs)

        valid_choices = [c[0] for c in self._meta.get_field('type').choices]
        if self.type not in valid_choices:
            self.type = 'other'

    def delete(self, *args, **kwargs):
        """
        On deletion, remove the folder named after the sanitized target name inside MEDIA_ROOT,
        if it exists, to clean up associated files.
        """

        # Sanitize folder name, same as when created (requires sanitize_filename function)
        safe_name = sanitize_filename(self.name)

        # Construct absolute folder path under MEDIA_ROOT
        folder_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, safe_name))
        media_root = os.path.abspath(settings.MEDIA_ROOT)

        # Safety check to ensure folder_path is within MEDIA_ROOT
        if folder_path.startswith(media_root) and os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

        # Call the parent class delete to remove the DB record
        super().delete(*args, **kwargs)

    @property
    def image_url(self):
        """
        Returns the full URL to the image if set, otherwise empty string.
        """
        if self.image:
            return os.path.join(settings.MEDIA_URL, self.image)
        return ""

    def __str__(self):
        # Return the target name for display
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Target"
        verbose_name_plural = "Targets"
        ordering = ['name']