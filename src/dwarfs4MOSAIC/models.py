import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models

from dwarfs4MOSAIC.utils import sanitize_filename

'''
__str__(self): shows how information is displayed when accessing an object from admin
'''


'''
Table 'observatory'
'''
class Tbl_observatory(models.Model):

    # fields
    name = models.CharField(
        max_length=200,
        verbose_name = "Name")

    website = models.URLField(
        blank=True,
        verbose_name = "Website",
        default="")

    location = models.CharField(
        max_length=200,
        verbose_name="Location",
        default="")

    longitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)])

    latitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)])

    altitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Altitude",
        help_text="meters")

    # telescopes:
    # One-to-many relationship is set in Tbl_telescope model.
    # It is not necessary to define it explicitly here, as Django handles it automatically.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observatory"
        verbose_name_plural = "Observatories"
        ordering = ['name']

'''
Table 'telescope'
'''
class Tbl_telescope(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name = "Name")

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Description")

    obs_tel = models.ForeignKey( #observatory where the telescope is located
        Tbl_observatory,
        on_delete=models.PROTECT,
        null=True,
        verbose_name = "Observatory")

    owner = models.TextField(
        default="",
        verbose_name = "Institutional Owner")

    aperture = models.FloatField(
        verbose_name="Aperture",
        default=0,
        validators=[MinValueValidator(0)],
        help_text="meters")

    status = models.CharField(
        choices=[
            ('unknown', 'Unknown'),
            ('operational', 'Operational'),
            ('inoperative', 'Inoperative'),
            ('maintenance', 'Under Maintenance')],
        max_length=11, #maximum length in choices
        default='unknown',
        verbose_name="Status")

    website = models.URLField(
        verbose_name="Website",
        blank=True,
        null=True,
        default="")

    # instrument:
    # One-to-many relationship is set in Tbl_instrument model.
    # It is not necessary to define it explicitly here, as Django handles it automatically.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Telescope"
        verbose_name_plural = "Telescopes"
        ordering = ['name']

'''
Table 'instrument'
'''
class Tbl_instrument(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name = "Name")

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Description")

    tel_ins = models.ForeignKey( # telescope where the instrument stands
        Tbl_telescope,
        on_delete=models.PROTECT,
        null=True,
        verbose_name = "Telescope")

    status = models.CharField(
        choices=[
            ('unknown', 'Unknown'),
            ('operational', 'Operational'),
            ('inoperative', 'Inoperative'),
            ('maintenance', 'Under Maintenance')],
        max_length=11,  # maximum length in choices
        default='unknown',
        verbose_name="Status")

    website = models.URLField(
        verbose_name="Website",
        blank=True,
        default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"
        ordering = ['name']

'''
Table 'researcher'
'''
class Tbl_researcher(models.Model):
    # Relates the researcher to a Django user (auth_user)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,  # If user is deleted, researcher is not!
        related_name='researcher',
        verbose_name="Username",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Name")

    email = models.EmailField(
        blank=True,
        verbose_name="email")

    @property
    def role(self):
        # Return group
        if not self.user.groups.exists():
            return ""
        else:
            return self.user.groups.first().name

    institution = models.CharField(
        max_length=200,
        default="",
        null=True,
        blank=True,
        verbose_name="Institution")

    is_phd = models.BooleanField(
        default=False,
        verbose_name="Is PhD")

    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    # observing_runs:
    # Many-to-many relationship is set in Tbl_observing_run model.
    # It is not necessary to define it explicitly here, as Django handles it automatically.

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Researcher"
        verbose_name_plural = "Researchers"
        ordering = ['user__username']

'''
Table 'observing_run'
'''
class Tbl_observing_run(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description")

    instrument = models.ForeignKey(
        Tbl_instrument,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Instrument")

    start_date = models.DateField(
        verbose_name="Start Date")

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="End Date")

    researchers = models.ManyToManyField(
        'Tbl_researcher',
        related_name='observing_runs'
    )

    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observing Run"
        verbose_name_plural = "Observing Runs"
        ordering = ['start_date']

'''
Table 'observing_block'
'''
class Tbl_observing_block(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    obs_run = models.ForeignKey(  # observing_run where the observing_block is executed
        Tbl_observing_run,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Observing Run")

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Description")
              
    start_time = models.DateTimeField( # date and time
        verbose_name="Start Time")
        
    end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="End Time")

    target = models.ManyToManyField(
        'Tbl_target',
        related_name='observing_blocks'
    )

    observation_mode = models.CharField(
        choices=[
            ('photometry', 'Photometry'),
            ('spectroscopy', 'Spectroscopy'),
            ('imaging', 'Imaging')],
        max_length=12,  # maximum length in choices
        default='photometry',
        verbose_name="Observation Mode")

    filters = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Filters")

    exposure_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Exposure Time",
        help_text="seconds")
        
    seeing = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Seeing",
        help_text="arcsec")
        
    weather_conditions = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Weather Conditions")
    
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observing Block"
        verbose_name_plural = "Observing Blocks"
        ordering = ['start_time']

'''
Table 'target'
'''
class Tbl_target(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Name")

    type = models.CharField(
        choices=[
            ('star', 'Star'),
            ('galaxy', 'Galaxy'),
            ('nebula', 'Nebula'),
            ('cluster', 'Star Cluster'),
            ('exoplanet', 'Exoplanet'),
            ('other', 'Other'),],
        max_length=9,  # maximum length in choices
        default='galaxy',
        verbose_name="Type")

    right_ascension = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Right Ascension",
        help_text="HH:MM:SS")

    declination = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Declination",
        help_text="+/- deg:min:sec")

    magnitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Magnitude",
        help_text="Referenced to Vega System")

    redshift = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Redshift (z)")

    size = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Size",
        help_text="arcsec",)

    semester = models.CharField(
        max_length=10,
        verbose_name="Visibility semester")

    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    image = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Image",
        editable=False,
        #help_text="Path relative to 'Dwarfs4MOSAIC/src/media'"
    )

    datafiles_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Data files path",
        editable=False,
        #help_text="Path relative to 'Dwarfs4MOSAIC/src/media'"
    )

    @property
    def image_name(self):
        if self.image and os.path.splitext(self.image)[1]:  # hay extensión de archivo
            return os.path.basename(self.image)
        return ""


    @property
    def relative_path(self):
        """
        Devuelve la ruta relativa desde MEDIA_ROOT a MEDIA_ROOT/safe_name.
        """
        safe_name = sanitize_filename(self.name)
        return safe_name

    @property
    def absolute_path(self):
        """
        Devuelve la ruta absoluta MEDIA_ROOT/safe_name.
        """
        return os.path.join(settings.MEDIA_ROOT, self.relative_path)


    def delete(self, *args, **kwargs):
        # Asegurar que usamos el nombre sanitizado igual que al crear
        safe_name = sanitize_filename(self.name)

        # Carpeta completa bajo MEDIA_ROOT
        folder_path = os.path.join(settings.MEDIA_ROOT, safe_name)

        # Seguridad: eliminar solo si está bajo MEDIA_ROOT
        folder_path = os.path.abspath(folder_path)
        media_root = os.path.abspath(settings.MEDIA_ROOT)

        if folder_path.startswith(media_root) and os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

        super().delete(*args, **kwargs)

    @property
    def image_url(self):
        return settings.MEDIA_URL + self.image

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Target"
        verbose_name_plural = "Targets"
        ordering = ['name']