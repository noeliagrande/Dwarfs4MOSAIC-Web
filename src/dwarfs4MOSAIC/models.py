from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observatory"
        verbose_name_plural = "Observatories"

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
        max_length=20,
        choices=[
            ('unknown', 'Unknown'),
            ('operational', 'Operational'),
            ('inoperative', 'Inoperative'),
            ('maintenance', 'Under Maintenance')],
        default='unknown',
        verbose_name="Status")

    website = models.URLField(
        verbose_name="Website",
        default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Telescope"
        verbose_name_plural = "Telescopes"

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
        max_length=20,
        choices=[
            ('unknown', 'Unknown'),
            ('operational', 'Operational'),
            ('inoperative', 'Inoperative'),
            ('maintenance', 'Under Maintenance')],
        default='unknown',
        verbose_name="Status")

    website = models.URLField(
        verbose_name="Website",
        default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"

'''
Table 'researcher'
'''
class Tbl_researcher(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    role = models.CharField(
        max_length=50,
        choices=[
            ('user', 'User'),
            ('core', 'Core')],
        default='user',
        verbose_name = "Role")

    institution = models.CharField(
        max_length=200,
        default="",
        verbose_name="Institution")

    email = models.EmailField(
        unique=True,
        verbose_name="email")

    # observing_runs, observing_blocks:
    # Many-to-many relationship is set in the Tbl_observing_run model.
    # It is not necessary to define it explicitly here, as Django handles it automatically.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Researcher"
        verbose_name_plural = "Researchers"

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

    #targets = models.ManyToManyField('Target', blank=True)

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observing Run"
        verbose_name_plural = "Observing Runs"

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
        max_length=50,
        choices=[('photometry', 'Photometry'), ('spectroscopy', 'Spectroscopy'), ('imaging', 'Imaging')],
        verbose_name="Observation Mode")

    filters = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Filters")

    exposure_time = models.DurationField(
        null=True, 
        blank=True,
        help_text="seconds",
        verbose_name="Exposure Time")
        
    seeing = models.FloatField(
        null=True, 
        blank=True, 
        help_text="arcseconds",
        verbose_name="Seeing")
        
    weather_conditions = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Weather Conditions")
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observing Block"
        verbose_name_plural = "Observing Blocks"

'''
Table 'target'
'''
class Tbl_target(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    type = models.CharField(
        max_length=50,
        choices=[
            ('star', 'Star'),
            ('galaxy', 'Galaxy'),
            ('nebula', 'Nebula'),
            ('cluster', 'Star Cluster'),
            ('exoplanet', 'Exoplanet'),
            ('other', 'Other'),],
        verbose_name="Type")

    right_ascension = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="HH:MM:SS",
        verbose_name="Right Ascension")

    declination = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="+/- deg:min:sec",
        verbose_name="Declination")

    magnitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Magnitude")

    redshift = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Redshift (z)")

    distance = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Distance (pc)")

    size = models.FloatField(
        null=True,
        blank=True,
        help_text="arcmin",
        verbose_name="Size")

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Target"
        verbose_name_plural = "Targets"