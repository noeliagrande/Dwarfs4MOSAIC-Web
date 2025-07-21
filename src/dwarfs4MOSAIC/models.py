"""
This file contains the Django model definitions for the main database tables
used in the project. Each model corresponds to a specific entity, such as
Observatory, Telescope, Instrument, Researcher, Observing Run, Observing Block,
and Target. These models define the database schema, relationships, and basic
behaviors for managing astronomical observation data.

Each form related to these models has its own detailed explanation and usage
notes, so please refer to the respective form documentation for specific field
descriptions and validation rules.
"""

# Standard libraries
import os
import shutil

# Third-party libraries
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Local application imports
from .utils import sanitize_filename

'''
__str__(self): shows how information is displayed when accessing an object from admin
'''


# --- 'observatory' table ---
class Tbl_observatory(models.Model):
    """
    Represents an astronomical observatory.
    Stores its name, website, location, coordinates, and altitude.
    """

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

# --- 'telescope' table ---
class Tbl_telescope(models.Model):
    """
    Represents a telescope located at an observatory.
    Stores details such as name, description, aperture, owner, status, and related observatory.
    """

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

# --- 'instrument' table ---
class Tbl_instrument(models.Model):
    """
    Represents an instrument installed on a telescope.
    Stores name, description, operational status, and related telescope.
    """

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

    def __str__(self):
        # Returns the instrument name when printed or displayed
        return self.name

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['name']

# --- 'researcher' table ---
class Tbl_researcher(models.Model):
    """
    Represents a researcher in the project.
    Linked to a Django user account and contains personal and role information.
    """

    # Links the researcher to a Django User object (auth_user)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,  # if User is deleted, the researcher remains
        related_name='researcher',
        verbose_name="Username",
        null=True,
        blank=True,
    )

    # Full name of the researcher
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    # Optional email address of the researcher
    email = models.EmailField(
        blank=True,
        verbose_name="email")

    # Role of the researcher in the project
    role = models.CharField(
        choices=[
            ('core_team', 'Core Team'),
            ('collaborator', 'Collaborator')],
        max_length=15,  # must be long enough to hold the longest choice
        default='collaborator',
        null=False,
        verbose_name="Role")

    # Institutional affiliation of the researcher
    institution = models.CharField(
        max_length=200,
        default="",
        null=True,
        blank=True,
        verbose_name="Institution")

    # Indicates whether the researcher is a PhD
    is_phd = models.BooleanField(
        default=False,
        verbose_name="Is PhD")

    # Additional notes or comments about the researcher
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    # Observing runs: Many-to-many relationship is defined in Tbl_observing_run.
    # Django automatically creates reverse accessors.

    # Observing blocks denied to this researcher
    denied_blocks = models.ManyToManyField(
        'Tbl_observing_block',
        blank=True,
        related_name='denied_researchers'
    )

    @property
    def display_name(self):
        # Returns the researcher's name, or a placeholder if not set
        return self.name or "(Name not assigned)"

    def __str__(self):
        # Returns a string representation of the researcher
        if self.name:
            return self.name
        elif self.user:
            return self.user.username
        return "(Unnamed Researcher)"

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Researcher"
        verbose_name_plural = "Researchers"
        ordering = ['user__username']

# --- 'observing_run' table ---
class Tbl_observing_run(models.Model):
    """
    Represents an observing run, a scheduled period of observations using
    a specific instrument. Includes details about dates, associated researchers,
    and optional comments.
    """

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

# --- 'observing_block' table ---
class Tbl_observing_block(models.Model):
    """
    Represents an observing block, a specific set of observations scheduled
    within an observing run. Includes timing, observation mode, targets,
    and environmental conditions.
    """

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

# --- 'target' table ---
class Tbl_target(models.Model):
    """
    Represents an astronomical target, such as a galaxy, calibration source, or other object.
    Includes positional data, observational parameters, and paths to associated files.
    """

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
    redshift = models.FloatField(
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